#!/usr/bin/env python3
"""
设计文档解析 MCP Server
支持直接从开发设计文档开始，跳过需求分析阶段
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

class DesignDocumentParser:
    """设计文档解析器"""
    
    def __init__(self):
        self.supported_formats = {
            "document": [".md", ".txt", ".docx", ".pdf"],
            "image": [".png", ".jpg", ".jpeg", ".bmp", ".gif"],
            "json": [".json"],
            "url": ["confluence", "notion", "wiki"]
        }
    
    def parse_design_document(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """解析设计文档，提取技术设计信息"""
        
        input_type = input_data.get("type", "")
        input_content = input_data.get("content", "")
        
        if input_type == "design_document_file":
            return self._parse_design_document_file(input_content)
        elif input_type == "design_document_url":
            return self._parse_design_document_url(input_content)
        elif input_type == "design_screenshots":
            return self._parse_design_screenshots(input_content)
        elif input_type == "direct_design_text":
            return self._parse_direct_design_text(input_content)
        else:
            return {"error": f"不支持的设计文档输入类型: {input_type}"}
    
    def _parse_design_document_file(self, file_path: str) -> Dict[str, Any]:
        """解析设计文档文件"""
        try:
            file = Path(file_path)
            if not file.exists():
                return {"error": f"设计文档文件不存在: {file_path}"}
            
            # 读取文档内容
            content = self._read_document_file(str(file))
            if not content:
                return {"error": "无法读取设计文档内容"}
            
            # 解析设计文档结构
            parsed_design = self._extract_design_elements(content)
            
            return {
                "source": "design_document_file",
                "file_path": file_path,
                "file_type": file.suffix.lower(),
                "raw_content": content,
                "parsed_design": parsed_design,
                "parsing_method": "document_analysis",
                "success": True
            }
            
        except Exception as e:
            return {
                "error": f"解析设计文档时出错: {str(e)}",
                "suggestion": "请检查文件格式和内容"
            }
    
    def _parse_direct_design_text(self, design_text: str) -> Dict[str, Any]:
        """解析直接输入的设计文档文本"""
        if not design_text.strip():
            return {"error": "设计文档内容为空"}
        
        # 解析设计文档结构
        parsed_design = self._extract_design_elements(design_text)
        
        return {
            "source": "direct_design_text",
            "raw_content": design_text.strip(),
            "parsed_design": parsed_design,
            "parsing_method": "text_analysis",
            "success": True
        }
    
    def _extract_design_elements(self, content: str) -> Dict[str, Any]:
        """从设计文档中提取设计要素"""
        
        design_elements = {
            "system_overview": self._extract_system_overview(content),
            "architecture_design": self._extract_architecture_design(content),
            "database_design": self._extract_database_design(content),
            "api_design": self._extract_api_design(content),
            "module_design": self._extract_module_design(content),
            "technology_stack": self._extract_technology_stack(content),
            "deployment_design": self._extract_deployment_design(content),
            "security_design": self._extract_security_design(content)
        }
        
        return design_elements
    
    def _extract_system_overview(self, content: str) -> Dict[str, Any]:
        """提取系统概述"""
        overview = {
            "project_name": "",
            "description": "",
            "objectives": [],
            "scope": ""
        }
        
        # 查找项目名称
        name_patterns = [
            r'项目名称[：:]\s*(.+?)(?=\n|$)',
            r'系统名称[：:]\s*(.+?)(?=\n|$)',
            r'# (.+?)系统',
            r'# (.+?)项目'
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                overview["project_name"] = match.group(1).strip()
                break
        
        # 查找项目描述
        desc_patterns = [
            r'项目描述[：:](.*?)(?=##|功能|架构|$)',
            r'系统概述[：:](.*?)(?=##|功能|架构|$)',
            r'概述[：:](.*?)(?=##|功能|架构|$)'
        ]
        
        for pattern in desc_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                overview["description"] = match.group(1).strip()
                break
        
        return overview
    
    def _extract_architecture_design(self, content: str) -> Dict[str, Any]:
        """提取架构设计"""
        architecture = {
            "architecture_pattern": "",
            "system_components": [],
            "layer_structure": {},
            "design_principles": []
        }
        
        # 查找架构模式
        arch_patterns = [
            r'架构模式[：:]\s*(.+?)(?=\n|$)',
            r'系统架构[：:]\s*(.+?)(?=\n|$)',
            r'采用(.+?)架构',
            r'使用(.+?)模式'
        ]
        
        for pattern in arch_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                architecture["architecture_pattern"] = match.group(1).strip()
                break
        
        # 查找系统组件
        component_patterns = [
            r'系统组件[：:](.*?)(?=##|数据库|API|$)',
            r'模块设计[：:](.*?)(?=##|数据库|API|$)',
            r'组件列表[：:](.*?)(?=##|数据库|API|$)'
        ]
        
        for pattern in component_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                component_text = match.group(1)
                # 提取组件列表
                components = re.findall(r'[-*]\s*(.+?)(?=\n|$)', component_text)
                architecture["system_components"] = [comp.strip() for comp in components]
                break
        
        return architecture
    
    def _extract_database_design(self, content: str) -> Dict[str, Any]:
        """提取数据库设计"""
        database = {
            "database_type": "",
            "tables": [],
            "relationships": [],
            "indexes": []
        }
        
        # 查找数据库类型
        db_patterns = [
            r'数据库[：:]\s*(.+?)(?=\n|$)',
            r'使用(.+?)数据库',
            r'存储[：:]\s*(.+?)(?=\n|$)'
        ]
        
        for pattern in db_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                database["database_type"] = match.group(1).strip()
                break
        
        # 查找表设计
        table_patterns = [
            r'表设计[：:](.*?)(?=##|API|接口|$)',
            r'数据表[：:](.*?)(?=##|API|接口|$)',
            r'表结构[：:](.*?)(?=##|API|接口|$)'
        ]
        
        for pattern in table_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                table_text = match.group(1)
                # 提取表名
                tables = re.findall(r'(?:表名|table)[：:]?\s*([a-zA-Z_][a-zA-Z0-9_]*)', table_text, re.IGNORECASE)
                database["tables"] = list(set(tables))
                break
        
        return database
    
    def _extract_api_design(self, content: str) -> Dict[str, Any]:
        """提取API设计"""
        api_design = {
            "api_style": "",
            "endpoints": [],
            "authentication": "",
            "data_format": ""
        }
        
        # 查找API风格
        api_patterns = [
            r'API[：:]\s*(.+?)(?=\n|$)',
            r'接口[：:]\s*(.+?)(?=\n|$)',
            r'采用(.+?)API',
            r'使用(.+?)接口'
        ]
        
        for pattern in api_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                api_design["api_style"] = match.group(1).strip()
                break
        
        # 查找接口端点
        endpoint_patterns = [
            r'接口列表[：:](.*?)(?=##|数据库|部署|$)',
            r'API端点[：:](.*?)(?=##|数据库|部署|$)',
            r'接口设计[：:](.*?)(?=##|数据库|部署|$)'
        ]
        
        for pattern in endpoint_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                endpoint_text = match.group(1)
                # 提取HTTP方法和路径
                endpoints = re.findall(r'(GET|POST|PUT|DELETE|PATCH)\s+([/\w\-{}]+)', endpoint_text, re.IGNORECASE)
                api_design["endpoints"] = [{"method": method.upper(), "path": path} for method, path in endpoints]
                break
        
        return api_design
    
    def _extract_module_design(self, content: str) -> List[Dict[str, Any]]:
        """提取模块设计"""
        modules = []
        
        # 查找模块定义
        module_patterns = [
            r'模块[：:]?\s*([a-zA-Z_][a-zA-Z0-9_]*)',
            r'组件[：:]?\s*([a-zA-Z_][a-zA-Z0-9_]*)',
            r'服务[：:]?\s*([a-zA-Z_][a-zA-Z0-9_]*)'
        ]
        
        found_modules = set()
        for pattern in module_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            found_modules.update(matches)
        
        for module_name in found_modules:
            modules.append({
                "name": module_name,
                "description": f"{module_name}模块",
                "responsibilities": []
            })
        
        return modules
    
    def _extract_technology_stack(self, content: str) -> Dict[str, List[str]]:
        """提取技术栈"""
        tech_stack = {
            "backend": [],
            "frontend": [],
            "database": [],
            "tools": []
        }
        
        # 查找技术栈信息
        tech_patterns = [
            r'技术栈[：:](.*?)(?=##|部署|安全|$)',
            r'技术选型[：:](.*?)(?=##|部署|安全|$)',
            r'开发技术[：:](.*?)(?=##|部署|安全|$)'
        ]
        
        for pattern in tech_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                tech_text = match.group(1)
                
                # 识别常见技术
                backend_techs = re.findall(r'(Spring Boot|Spring|Java|Python|Node\.js|Go|\.NET)', tech_text, re.IGNORECASE)
                frontend_techs = re.findall(r'(Vue\.js|React|Angular|jQuery|Bootstrap)', tech_text, re.IGNORECASE)
                database_techs = re.findall(r'(MySQL|PostgreSQL|OceanBase|Redis|MongoDB)', tech_text, re.IGNORECASE)
                
                tech_stack["backend"] = list(set(backend_techs))
                tech_stack["frontend"] = list(set(frontend_techs))
                tech_stack["database"] = list(set(database_techs))
                break
        
        return tech_stack
    
    def _extract_deployment_design(self, content: str) -> Dict[str, Any]:
        """提取部署设计"""
        deployment = {
            "deployment_method": "",
            "environment": [],
            "infrastructure": []
        }
        
        # 查找部署方式
        deploy_patterns = [
            r'部署[：:]\s*(.+?)(?=\n|$)',
            r'部署方式[：:]\s*(.+?)(?=\n|$)',
            r'环境[：:]\s*(.+?)(?=\n|$)'
        ]
        
        for pattern in deploy_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                deployment["deployment_method"] = match.group(1).strip()
                break
        
        return deployment
    
    def _extract_security_design(self, content: str) -> Dict[str, Any]:
        """提取安全设计"""
        security = {
            "authentication": "",
            "authorization": "",
            "data_protection": [],
            "security_measures": []
        }
        
        # 查找安全相关信息
        security_patterns = [
            r'安全[：:](.*?)(?=##|部署|总结|$)',
            r'权限[：:](.*?)(?=##|部署|总结|$)',
            r'认证[：:](.*?)(?=##|部署|总结|$)'
        ]
        
        for pattern in security_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                security_text = match.group(1)
                
                # 提取安全措施
                measures = re.findall(r'[-*]\s*(.+?)(?=\n|$)', security_text)
                security["security_measures"] = [measure.strip() for measure in measures]
                break
        
        return security
    
    def _read_document_file(self, file_path: str) -> str:
        """读取文档文件"""
        file = Path(file_path)
        file_ext = file.suffix.lower()
        
        try:
            if file_ext == ".md" or file_ext == ".txt":
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            elif file_ext == ".json":
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return json.dumps(data, indent=2, ensure_ascii=False)
            elif file_ext == ".docx":
                try:
                    from docx import Document
                    doc = Document(file_path)
                    content = []
                    for paragraph in doc.paragraphs:
                        content.append(paragraph.text)
                    return '\n'.join(content)
                except ImportError:
                    return "[需要安装python-docx库来读取Word文档]"
            else:
                return ""
        except Exception as e:
            return f"[读取文件失败: {e}]"
    
    def generate_implementation_plan(self, parsed_design: Dict[str, Any]) -> Dict[str, Any]:
        """基于设计文档生成实施计划"""
        
        plan = {
            "development_phases": [],
            "module_priorities": [],
            "technical_tasks": [],
            "estimated_timeline": {}
        }
        
        # 根据模块设计生成开发阶段
        modules = parsed_design.get("module_design", [])
        if modules:
            for i, module in enumerate(modules):
                plan["development_phases"].append({
                    "phase": i + 1,
                    "name": f"{module['name']}模块开发",
                    "description": f"实现{module['name']}相关功能",
                    "deliverables": [
                        f"{module['name']}实体类",
                        f"{module['name']}业务逻辑",
                        f"{module['name']}API接口",
                        f"{module['name']}测试用例"
                    ]
                })
        
        # 生成技术任务
        tech_stack = parsed_design.get("technology_stack", {})
        if tech_stack:
            plan["technical_tasks"].extend([
                "项目架构搭建",
                "数据库设计实现",
                "基础框架配置",
                "安全机制实现",
                "API接口开发",
                "前端界面开发",
                "测试用例编写",
                "部署配置"
            ])
        
        return plan

# MCP Server 主函数
def main():
    """MCP Server 主入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python 设计文档解析MCP工具.py <input_data_json>")
        print("支持的输入格式:")
        print("1. 设计文档文件: {'type': 'design_document_file', 'content': '/path/to/design.md'}")
        print("2. 设计文档URL: {'type': 'design_document_url', 'content': 'https://...'}")
        print("3. 设计截图: {'type': 'design_screenshots', 'content': '/path/to/screenshots'}")
        print("4. 直接文本: {'type': 'direct_design_text', 'content': '设计文档内容...'}")
        sys.exit(1)
    
    input_data_json = sys.argv[1]
    
    try:
        input_data = json.loads(input_data_json)
    except json.JSONDecodeError:
        print("Invalid input JSON format")
        sys.exit(1)
    
    parser = DesignDocumentParser()
    
    # 解析设计文档
    result = parser.parse_design_document(input_data)
    
    # 如果解析成功，生成实施计划
    if result.get("success") and "parsed_design" in result:
        implementation_plan = parser.generate_implementation_plan(result["parsed_design"])
        result["implementation_plan"] = implementation_plan
    
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
