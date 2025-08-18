#!/usr/bin/env python3
"""
架构设计 MCP Server
基于需求分析和用户故事生成系统架构设计
"""

import json
from typing import Dict, List, Any

class ArchitectureDesigner:
    """架构设计器"""
    
    def __init__(self):
        self.design_patterns = self._load_design_patterns()
    
    def design_system_architecture(self, requirements_analysis: Dict[str, Any], 
                                 user_stories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """设计系统架构"""
        
        # 分析复杂度和规模
        complexity_analysis = self._analyze_system_complexity(requirements_analysis, user_stories)
        
        # 选择架构模式
        architecture_pattern = self._select_architecture_pattern(complexity_analysis)
        
        # 设计系统组件
        system_components = self._design_system_components(requirements_analysis, architecture_pattern)
        
        # 设计数据流
        data_flow = self._design_data_flow(system_components, user_stories)
        
        # 设计部署架构
        deployment_architecture = self._design_deployment_architecture(architecture_pattern, complexity_analysis)
        
        # 技术栈推荐
        technology_stack = self._recommend_technology_stack(architecture_pattern, requirements_analysis)
        
        architecture_design = {
            "complexity_analysis": complexity_analysis,
            "architecture_pattern": architecture_pattern,
            "system_components": system_components,
            "data_flow": data_flow,
            "deployment_architecture": deployment_architecture,
            "technology_stack": technology_stack,
            "design_principles": self._define_design_principles(),
            "quality_attributes": self._define_quality_attributes(requirements_analysis)
        }
        
        return architecture_design
    
    def _analyze_system_complexity(self, requirements_analysis: Dict[str, Any], 
                                 user_stories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析系统复杂度"""
        
        functional_reqs = requirements_analysis.get("functional_requirements", [])
        data_entities = requirements_analysis.get("data_entities", [])
        user_roles = requirements_analysis.get("user_roles", [])
        
        total_story_points = sum(story.get("story_points", 0) for story in user_stories)
        
        complexity_score = 0
        complexity_factors = []
        
        # 功能复杂度
        if len(functional_reqs) > 20:
            complexity_score += 3
            complexity_factors.append("功能需求数量较多")
        elif len(functional_reqs) > 10:
            complexity_score += 2
            complexity_factors.append("功能需求数量中等")
        else:
            complexity_score += 1
            complexity_factors.append("功能需求数量较少")
        
        # 数据复杂度
        if len(data_entities) > 15:
            complexity_score += 3
            complexity_factors.append("数据实体较多，关系复杂")
        elif len(data_entities) > 8:
            complexity_score += 2
            complexity_factors.append("数据实体中等")
        else:
            complexity_score += 1
            complexity_factors.append("数据实体较少")
        
        # 用户角色复杂度
        if len(user_roles) > 5:
            complexity_score += 2
            complexity_factors.append("用户角色多样化")
        elif len(user_roles) > 2:
            complexity_score += 1
            complexity_factors.append("用户角色适中")
        
        # 故事点复杂度
        if total_story_points > 100:
            complexity_score += 3
            complexity_factors.append("开发工作量大")
        elif total_story_points > 50:
            complexity_score += 2
            complexity_factors.append("开发工作量中等")
        else:
            complexity_score += 1
            complexity_factors.append("开发工作量较小")
        
        # 确定复杂度等级
        if complexity_score >= 10:
            complexity_level = "高"
        elif complexity_score >= 6:
            complexity_level = "中"
        else:
            complexity_level = "低"
        
        return {
            "complexity_level": complexity_level,
            "complexity_score": complexity_score,
            "complexity_factors": complexity_factors,
            "metrics": {
                "functional_requirements": len(functional_reqs),
                "data_entities": len(data_entities),
                "user_roles": len(user_roles),
                "total_story_points": total_story_points
            }
        }
    
    def _select_architecture_pattern(self, complexity_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """选择架构模式"""
        
        complexity_level = complexity_analysis["complexity_level"]
        
        if complexity_level == "高":
            return {
                "primary_pattern": "微服务架构",
                "secondary_patterns": ["领域驱动设计", "CQRS"],
                "rationale": "系统复杂度高，采用微服务架构便于团队协作和系统维护",
                "benefits": [
                    "服务独立部署和扩展",
                    "技术栈多样化",
                    "团队独立开发",
                    "故障隔离"
                ],
                "challenges": [
                    "分布式系统复杂性",
                    "服务间通信开销",
                    "数据一致性",
                    "运维复杂度"
                ]
            }
        
        elif complexity_level == "中":
            return {
                "primary_pattern": "分层架构",
                "secondary_patterns": ["六边形架构", "领域驱动设计"],
                "rationale": "系统复杂度适中，采用分层架构平衡开发效率和可维护性",
                "benefits": [
                    "结构清晰易理解",
                    "开发效率高",
                    "技术栈统一",
                    "团队协作简单"
                ],
                "challenges": [
                    "单体应用扩展限制",
                    "技术栈绑定",
                    "部署粒度粗"
                ]
            }
        
        else:
            return {
                "primary_pattern": "简单分层架构",
                "secondary_patterns": ["MVC"],
                "rationale": "系统复杂度较低，采用简单架构快速交付",
                "benefits": [
                    "开发速度快",
                    "学习成本低",
                    "部署简单",
                    "维护成本低"
                ],
                "challenges": [
                    "扩展性有限",
                    "功能耦合度高"
                ]
            }
    
    def _design_system_components(self, requirements_analysis: Dict[str, Any], 
                                architecture_pattern: Dict[str, Any]) -> List[Dict[str, Any]]:
        """设计系统组件"""
        
        components = []
        data_entities = requirements_analysis.get("data_entities", [])
        primary_pattern = architecture_pattern["primary_pattern"]
        
        if primary_pattern == "微服务架构":
            # 为每个主要数据实体创建微服务
            for entity in data_entities:
                service_name = f"{entity['name']}服务"
                components.append({
                    "name": service_name,
                    "type": "微服务",
                    "responsibilities": [
                        f"{entity['name']}数据管理",
                        f"{entity['name']}业务逻辑处理",
                        f"{entity['name']}相关API提供"
                    ],
                    "interfaces": [
                        f"{entity['name']} REST API",
                        f"{entity['name']} 事件发布"
                    ],
                    "dependencies": ["数据库", "消息队列"],
                    "technology": "Spring Boot + Spring Data JPA"
                })
            
            # 添加网关服务
            components.append({
                "name": "API网关",
                "type": "基础设施服务",
                "responsibilities": [
                    "请求路由",
                    "认证授权",
                    "限流熔断",
                    "监控日志"
                ],
                "interfaces": ["HTTP API"],
                "dependencies": ["各微服务"],
                "technology": "Spring Cloud Gateway"
            })
            
        elif primary_pattern in ["分层架构", "简单分层架构"]:
            # 分层架构组件
            layers = [
                {
                    "name": "表现层",
                    "type": "应用层",
                    "responsibilities": [
                        "用户界面展示",
                        "用户交互处理",
                        "请求响应处理"
                    ],
                    "components": ["Controller", "REST API", "Web页面"]
                },
                {
                    "name": "业务逻辑层",
                    "type": "业务层",
                    "responsibilities": [
                        "业务规则实现",
                        "业务流程控制",
                        "事务管理"
                    ],
                    "components": ["Service", "业务对象", "工作流引擎"]
                },
                {
                    "name": "数据访问层",
                    "type": "数据层",
                    "responsibilities": [
                        "数据持久化",
                        "数据查询",
                        "缓存管理"
                    ],
                    "components": ["Repository", "DAO", "缓存"]
                },
                {
                    "name": "数据库层",
                    "type": "存储层",
                    "responsibilities": [
                        "数据存储",
                        "数据完整性",
                        "并发控制"
                    ],
                    "components": ["关系数据库", "NoSQL数据库"]
                }
            ]
            
            components.extend(layers)
        
        return components
    
    def _design_data_flow(self, system_components: List[Dict[str, Any]], 
                         user_stories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """设计数据流"""
        
        # 分析主要的数据流场景
        data_flows = []
        
        # 从用户故事中提取数据流
        for story in user_stories:
            if "创建" in story.get("i_want", ""):
                data_flows.append({
                    "scenario": f"{story['as_a']}创建数据",
                    "flow": [
                        "用户输入数据",
                        "表现层接收请求",
                        "业务层验证数据",
                        "数据层持久化",
                        "返回创建结果"
                    ]
                })
            
            elif "查询" in story.get("i_want", "") or "查看" in story.get("i_want", ""):
                data_flows.append({
                    "scenario": f"{story['as_a']}查询数据",
                    "flow": [
                        "用户发起查询",
                        "表现层接收请求",
                        "业务层处理查询逻辑",
                        "数据层执行查询",
                        "返回查询结果"
                    ]
                })
        
        return {
            "data_flows": data_flows,
            "data_consistency_strategy": "强一致性",
            "caching_strategy": "多级缓存",
            "backup_strategy": "定期备份 + 实时同步"
        }
    
    def _design_deployment_architecture(self, architecture_pattern: Dict[str, Any], 
                                      complexity_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """设计部署架构"""
        
        primary_pattern = architecture_pattern["primary_pattern"]
        complexity_level = complexity_analysis["complexity_level"]
        
        if primary_pattern == "微服务架构":
            return {
                "deployment_pattern": "容器化部署",
                "infrastructure": {
                    "container_platform": "Docker + Kubernetes",
                    "service_mesh": "Istio",
                    "monitoring": "Prometheus + Grafana",
                    "logging": "ELK Stack",
                    "ci_cd": "Jenkins + GitLab CI"
                },
                "environments": [
                    {
                        "name": "开发环境",
                        "resources": "2 CPU, 4GB RAM per service",
                        "replicas": 1
                    },
                    {
                        "name": "测试环境", 
                        "resources": "2 CPU, 4GB RAM per service",
                        "replicas": 2
                    },
                    {
                        "name": "生产环境",
                        "resources": "4 CPU, 8GB RAM per service",
                        "replicas": 3
                    }
                ]
            }
        
        else:
            return {
                "deployment_pattern": "传统部署",
                "infrastructure": {
                    "application_server": "Tomcat/Spring Boot",
                    "web_server": "Nginx",
                    "database": "OceanBase",
                    "monitoring": "Spring Boot Actuator",
                    "ci_cd": "Jenkins"
                },
                "environments": [
                    {
                        "name": "开发环境",
                        "resources": "4 CPU, 8GB RAM",
                        "instances": 1
                    },
                    {
                        "name": "测试环境",
                        "resources": "4 CPU, 8GB RAM", 
                        "instances": 1
                    },
                    {
                        "name": "生产环境",
                        "resources": "8 CPU, 16GB RAM",
                        "instances": 2
                    }
                ]
            }
    
    def _recommend_technology_stack(self, architecture_pattern: Dict[str, Any], 
                                  requirements_analysis: Dict[str, Any]) -> Dict[str, List[str]]:
        """推荐技术栈"""
        
        primary_pattern = architecture_pattern["primary_pattern"]
        
        if primary_pattern == "微服务架构":
            return {
                "backend_framework": ["Spring Boot", "Spring Cloud"],
                "database": ["OceanBase", "Redis", "MongoDB"],
                "message_queue": ["RabbitMQ", "Apache Kafka"],
                "service_discovery": ["Eureka", "Consul"],
                "api_gateway": ["Spring Cloud Gateway", "Zuul"],
                "monitoring": ["Prometheus", "Grafana", "Zipkin"],
                "container": ["Docker", "Kubernetes"],
                "frontend": ["Vue.js", "React"],
                "build_tools": ["Maven", "Gradle"]
            }
        
        else:
            return {
                "backend_framework": ["Spring Boot", "Spring MVC"],
                "database": ["OceanBase", "Redis"],
                "orm": ["Spring Data JPA", "MyBatis"],
                "security": ["Spring Security"],
                "frontend": ["Vue.js", "Element UI"],
                "build_tools": ["Maven"],
                "testing": ["JUnit 5", "Mockito"],
                "documentation": ["Swagger", "Spring REST Docs"]
            }
    
    def _define_design_principles(self) -> List[str]:
        """定义设计原则"""
        return [
            "单一职责原则 - 每个组件只负责一个功能",
            "开闭原则 - 对扩展开放，对修改关闭",
            "依赖倒置原则 - 依赖抽象而不是具体实现",
            "接口隔离原则 - 使用多个专门的接口",
            "最少知识原则 - 减少组件间的耦合",
            "DRY原则 - 不要重复自己",
            "KISS原则 - 保持简单愚蠢"
        ]
    
    def _define_quality_attributes(self, requirements_analysis: Dict[str, Any]) -> Dict[str, str]:
        """定义质量属性"""
        non_functional_reqs = requirements_analysis.get("non_functional_requirements", [])
        
        quality_attributes = {
            "performance": "响应时间 < 2秒，吞吐量 > 1000 TPS",
            "scalability": "支持水平扩展，处理用户增长",
            "availability": "系统可用性 > 99.9%",
            "security": "数据加密，访问控制，审计日志",
            "maintainability": "代码可读性好，模块化设计",
            "testability": "单元测试覆盖率 > 80%",
            "usability": "界面友好，操作简单"
        }
        
        # 根据非功能需求调整质量属性
        for nfr in non_functional_reqs:
            category = nfr.get("category", "")
            if category == "performance":
                quality_attributes["performance"] = nfr.get("measurable", quality_attributes["performance"])
            elif category == "security":
                quality_attributes["security"] = nfr.get("measurable", quality_attributes["security"])
        
        return quality_attributes
    
    def _load_design_patterns(self) -> Dict[str, Any]:
        """加载设计模式"""
        return {
            "creational": ["单例模式", "工厂模式", "建造者模式"],
            "structural": ["适配器模式", "装饰器模式", "外观模式"],
            "behavioral": ["观察者模式", "策略模式", "命令模式"]
        }

# MCP Server 主函数
def main():
    """MCP Server 主入口"""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python 架构设计MCP工具.py <requirements_analysis_json> <user_stories_json>")
        sys.exit(1)
    
    requirements_analysis_json = sys.argv[1]
    user_stories_json = sys.argv[2]
    
    try:
        requirements_analysis = json.loads(requirements_analysis_json)
        user_stories = json.loads(user_stories_json)
    except json.JSONDecodeError:
        print("Invalid JSON format")
        sys.exit(1)
    
    designer = ArchitectureDesigner()
    architecture_design = designer.design_system_architecture(requirements_analysis, user_stories)
    
    print(json.dumps(architecture_design, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
