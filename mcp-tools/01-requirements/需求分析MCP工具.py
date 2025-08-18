#!/usr/bin/env python3
"""
需求分析 MCP Server
将产品需求转化为技术需求和功能规格
"""

import json
import re
from typing import Dict, List, Any
from pathlib import Path

class RequirementsAnalyzer:
    """需求分析器"""
    
    def __init__(self):
        self.analysis_result = {}
    
    def analyze_product_requirements(self, requirements_text: str) -> Dict[str, Any]:
        """分析产品需求文档"""
        analysis = {
            "functional_requirements": self._extract_functional_requirements(requirements_text),
            "non_functional_requirements": self._extract_non_functional_requirements(requirements_text),
            "user_roles": self._identify_user_roles(requirements_text),
            "business_rules": self._extract_business_rules(requirements_text),
            "data_entities": self._identify_data_entities(requirements_text),
            "api_requirements": self._extract_api_requirements(requirements_text),
            "technical_constraints": self._identify_technical_constraints(requirements_text),
            "acceptance_criteria": self._generate_acceptance_criteria(requirements_text)
        }
        
        self.analysis_result = analysis
        return analysis
    
    def _extract_functional_requirements(self, text: str) -> List[Dict[str, str]]:
        """提取功能性需求"""
        functional_reqs = []
        
        # 查找功能描述模式
        patterns = [
            r'用户可以(.+?)(?=。|$)',
            r'系统应该(.+?)(?=。|$)',
            r'功能[：:](.+?)(?=。|$)',
            r'需要实现(.+?)(?=。|$)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                functional_reqs.append({
                    "id": f"FR-{len(functional_reqs) + 1:03d}",
                    "description": match.strip(),
                    "priority": self._determine_priority(match),
                    "complexity": self._estimate_complexity(match)
                })
        
        return functional_reqs
    
    def _extract_non_functional_requirements(self, text: str) -> List[Dict[str, str]]:
        """提取非功能性需求"""
        non_functional_reqs = []
        
        # 性能需求
        performance_patterns = [
            r'响应时间(.+?)(?=。|$)',
            r'并发(.+?)(?=。|$)',
            r'性能(.+?)(?=。|$)'
        ]
        
        # 安全需求
        security_patterns = [
            r'安全(.+?)(?=。|$)',
            r'权限(.+?)(?=。|$)',
            r'认证(.+?)(?=。|$)'
        ]
        
        # 可用性需求
        usability_patterns = [
            r'可用性(.+?)(?=。|$)',
            r'易用(.+?)(?=。|$)',
            r'用户体验(.+?)(?=。|$)'
        ]
        
        all_patterns = [
            ("performance", performance_patterns),
            ("security", security_patterns),
            ("usability", usability_patterns)
        ]
        
        for category, patterns in all_patterns:
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    non_functional_reqs.append({
                        "id": f"NFR-{len(non_functional_reqs) + 1:03d}",
                        "category": category,
                        "description": match.strip(),
                        "measurable": self._make_measurable(match, category)
                    })
        
        return non_functional_reqs
    
    def _identify_user_roles(self, text: str) -> List[Dict[str, str]]:
        """识别用户角色"""
        roles = []
        
        # 角色识别模式
        role_patterns = [
            r'([管理员|用户|客户|操作员|审核员|系统管理员]+)',
            r'([A-Za-z]+(?:管理员|用户|员))',
            r'作为(.+?)(?=，|。|$)'
        ]
        
        found_roles = set()
        for pattern in role_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                role_name = match.strip()
                if role_name and len(role_name) < 20:  # 过滤过长的匹配
                    found_roles.add(role_name)
        
        for role in found_roles:
            roles.append({
                "name": role,
                "description": f"{role}的系统使用者",
                "permissions": self._infer_permissions(role, text)
            })
        
        return roles
    
    def _extract_business_rules(self, text: str) -> List[Dict[str, str]]:
        """提取业务规则"""
        business_rules = []
        
        # 业务规则模式
        rule_patterns = [
            r'规则[：:](.+?)(?=。|$)',
            r'必须(.+?)(?=。|$)',
            r'不能(.+?)(?=。|$)',
            r'当(.+?)时(.+?)(?=。|$)',
            r'如果(.+?)则(.+?)(?=。|$)'
        ]
        
        for pattern in rule_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    rule_desc = " ".join(match)
                else:
                    rule_desc = match
                
                business_rules.append({
                    "id": f"BR-{len(business_rules) + 1:03d}",
                    "description": rule_desc.strip(),
                    "type": self._classify_rule_type(rule_desc)
                })
        
        return business_rules
    
    def _identify_data_entities(self, text: str) -> List[Dict[str, Any]]:
        """识别数据实体"""
        entities = []
        
        # 实体识别模式
        entity_patterns = [
            r'([用户|订单|商品|产品|客户|账户|支付|地址|评价|库存]+)信息',
            r'([用户|订单|商品|产品|客户|账户|支付|地址|评价|库存]+)数据',
            r'([用户|订单|商品|产品|客户|账户|支付|地址|评价|库存]+)管理',
            r'([A-Za-z]+)表',
            r'([A-Za-z]+)实体'
        ]
        
        found_entities = set()
        for pattern in entity_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                entity_name = match.strip()
                if entity_name and len(entity_name) < 10:
                    found_entities.add(entity_name)
        
        for entity in found_entities:
            entities.append({
                "name": entity,
                "description": f"{entity}相关的数据实体",
                "attributes": self._infer_attributes(entity, text),
                "relationships": []
            })
        
        return entities
    
    def _extract_api_requirements(self, text: str) -> List[Dict[str, str]]:
        """提取API需求"""
        api_reqs = []
        
        # API需求模式
        api_patterns = [
            r'接口(.+?)(?=。|$)',
            r'API(.+?)(?=。|$)',
            r'查询(.+?)(?=。|$)',
            r'创建(.+?)(?=。|$)',
            r'更新(.+?)(?=。|$)',
            r'删除(.+?)(?=。|$)'
        ]
        
        for pattern in api_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                api_reqs.append({
                    "endpoint": self._generate_endpoint(match),
                    "method": self._determine_http_method(match),
                    "description": match.strip(),
                    "parameters": self._extract_parameters(match)
                })
        
        return api_reqs
    
    def generate_technical_specification(self) -> Dict[str, Any]:
        """生成技术规格说明"""
        if not self.analysis_result:
            return {"error": "请先执行需求分析"}
        
        tech_spec = {
            "project_overview": self._generate_project_overview(),
            "system_architecture": self._recommend_architecture(),
            "technology_stack": self._recommend_technology_stack(),
            "database_design": self._generate_database_outline(),
            "api_specification": self._generate_api_specification(),
            "development_phases": self._plan_development_phases(),
            "risk_assessment": self._assess_risks()
        }
        
        return tech_spec
    
    def _generate_project_overview(self) -> Dict[str, str]:
        """生成项目概述"""
        functional_count = len(self.analysis_result.get("functional_requirements", []))
        entities_count = len(self.analysis_result.get("data_entities", []))
        roles_count = len(self.analysis_result.get("user_roles", []))
        
        return {
            "description": "基于需求分析生成的项目概述",
            "scope": f"包含{functional_count}个功能需求，{entities_count}个数据实体，{roles_count}个用户角色",
            "objectives": "实现业务需求的数字化管理系统"
        }
    
    def _recommend_architecture(self) -> Dict[str, str]:
        """推荐系统架构"""
        functional_count = len(self.analysis_result.get("functional_requirements", []))
        
        if functional_count > 20:
            return {
                "pattern": "微服务架构",
                "reason": "功能复杂度较高，建议采用微服务架构便于维护和扩展"
            }
        elif functional_count > 10:
            return {
                "pattern": "分层架构",
                "reason": "中等复杂度，采用经典分层架构平衡开发效率和可维护性"
            }
        else:
            return {
                "pattern": "简单分层架构",
                "reason": "功能相对简单，采用简单分层架构快速开发"
            }
    
    def _recommend_technology_stack(self) -> Dict[str, List[str]]:
        """推荐技术栈"""
        return {
            "backend": ["Spring Boot", "Spring Data JPA", "Spring Security"],
            "database": ["OceanBase", "Redis"],
            "frontend": ["Vue.js", "Element UI"],
            "tools": ["Maven", "Docker", "Jenkins"]
        }
    
    # 辅助方法
    def _determine_priority(self, requirement: str) -> str:
        """确定需求优先级"""
        high_keywords = ["必须", "核心", "关键", "重要"]
        medium_keywords = ["应该", "需要", "建议"]
        
        for keyword in high_keywords:
            if keyword in requirement:
                return "高"
        
        for keyword in medium_keywords:
            if keyword in requirement:
                return "中"
        
        return "低"
    
    def _estimate_complexity(self, requirement: str) -> str:
        """估算复杂度"""
        complex_keywords = ["复杂", "算法", "集成", "同步", "批量"]
        simple_keywords = ["查询", "显示", "列表", "基本"]
        
        for keyword in complex_keywords:
            if keyword in requirement:
                return "高"
        
        for keyword in simple_keywords:
            if keyword in requirement:
                return "低"
        
        return "中"
    
    def _make_measurable(self, requirement: str, category: str) -> str:
        """使非功能需求可度量"""
        if category == "performance":
            return "响应时间 < 2秒，并发用户 > 1000"
        elif category == "security":
            return "通过安全测试，无高危漏洞"
        elif category == "usability":
            return "用户满意度 > 4.0/5.0"
        return requirement

# MCP Server 主函数
def main():
    """MCP Server 主入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python 需求分析MCP工具.py <requirements_text>")
        sys.exit(1)
    
    requirements_text = sys.argv[1]
    analyzer = RequirementsAnalyzer()
    
    # 分析需求
    analysis_result = analyzer.analyze_product_requirements(requirements_text)
    
    # 生成技术规格
    tech_spec = analyzer.generate_technical_specification()
    
    result = {
        "requirements_analysis": analysis_result,
        "technical_specification": tech_spec
    }
    
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
