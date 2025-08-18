#!/usr/bin/env python3
"""
设计文档生成 MCP Server
基于需求分析结果生成完整的技术设计文档
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

class DesignDocumentGenerator:
    """设计文档生成器"""
    
    def __init__(self):
        self.template_sections = [
            "system_overview",
            "architecture_design", 
            "database_design",
            "api_design",
            "module_design",
            "technology_stack",
            "security_design",
            "deployment_design",
            "performance_design"
        ]
    
    def generate_design_document(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """基于需求分析结果生成设计文档"""
        
        try:
            requirements_analysis = input_data.get("requirements_analysis", {})
            user_stories = input_data.get("user_stories", [])
            architecture_design = input_data.get("architecture_design", {})
            project_context = input_data.get("project_context", {})
            
            # 生成设计文档内容
            design_document = self._generate_document_content(
                requirements_analysis, user_stories, architecture_design, project_context
            )
            
            # 生成Markdown格式文档
            markdown_content = self._generate_markdown_document(design_document)
            
            return {
                "success": True,
                "design_document": design_document,
                "markdown_content": markdown_content,
                "generation_method": "requirements_based",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "error": f"生成设计文档时出错: {str(e)}",
                "success": False
            }
    
    def _generate_document_content(self, requirements: Dict, user_stories: List, 
                                 architecture: Dict, context: Dict) -> Dict[str, Any]:
        """生成设计文档内容"""
        
        document = {
            "metadata": self._generate_metadata(requirements, context),
            "system_overview": self._generate_system_overview(requirements, context),
            "architecture_design": self._generate_architecture_design(architecture, requirements),
            "database_design": self._generate_database_design(requirements, user_stories),
            "api_design": self._generate_api_design(requirements, user_stories),
            "module_design": self._generate_module_design(requirements, user_stories),
            "technology_stack": self._generate_technology_stack(architecture, context),
            "security_design": self._generate_security_design(requirements),
            "deployment_design": self._generate_deployment_design(architecture),
            "performance_design": self._generate_performance_design(requirements)
        }
        
        return document
    
    def _generate_metadata(self, requirements: Dict, context: Dict) -> Dict[str, Any]:
        """生成文档元数据"""
        return {
            "document_title": f"{context.get('project_name', '系统')}技术设计文档",
            "version": "1.0",
            "author": "AI代码生成系统",
            "created_date": datetime.now().strftime("%Y-%m-%d"),
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "project_name": context.get("project_name", ""),
            "project_description": requirements.get("project_description", "")
        }
    
    def _generate_system_overview(self, requirements: Dict, context: Dict) -> Dict[str, Any]:
        """生成系统概述"""
        
        functional_requirements = requirements.get("functional_requirements", [])
        non_functional_requirements = requirements.get("non_functional_requirements", [])
        
        return {
            "project_name": context.get("project_name", ""),
            "description": requirements.get("project_description", ""),
            "objectives": [req.get("description", "") for req in functional_requirements[:5]],
            "scope": {
                "included": [req.get("title", "") for req in functional_requirements],
                "excluded": ["暂无明确排除项"]
            },
            "stakeholders": requirements.get("user_roles", []),
            "success_criteria": [req.get("description", "") for req in non_functional_requirements]
        }
    
    def _generate_architecture_design(self, architecture: Dict, requirements: Dict) -> Dict[str, Any]:
        """生成架构设计"""
        
        return {
            "architecture_pattern": architecture.get("architecture_pattern", "分层架构"),
            "design_principles": [
                "单一职责原则",
                "开闭原则", 
                "依赖倒置原则",
                "接口隔离原则"
            ],
            "system_components": architecture.get("components", [
                {"name": "表现层", "description": "处理HTTP请求和响应"},
                {"name": "业务逻辑层", "description": "实现业务规则和流程"},
                {"name": "数据访问层", "description": "封装数据访问逻辑"},
                {"name": "数据库层", "description": "数据持久化存储"}
            ]),
            "layer_structure": {
                "presentation": "Controller层 - 处理HTTP请求",
                "business": "Service层 - 业务逻辑处理", 
                "persistence": "Repository层 - 数据访问",
                "database": "数据库层 - 数据存储"
            },
            "communication_patterns": [
                "同步调用：层间直接调用",
                "异步消息：事件驱动处理",
                "RESTful API：外部接口"
            ]
        }
    
    def _generate_database_design(self, requirements: Dict, user_stories: List) -> Dict[str, Any]:
        """生成数据库设计"""
        
        # 从需求中提取实体
        entities = self._extract_entities_from_requirements(requirements, user_stories)
        
        return {
            "database_type": "MySQL 8.0",
            "charset": "utf8mb4",
            "storage_engine": "InnoDB",
            "entities": entities,
            "tables": self._generate_table_designs(entities),
            "relationships": self._generate_relationships(entities),
            "indexes": self._generate_indexes(entities),
            "constraints": [
                "外键约束确保数据完整性",
                "唯一约束防止重复数据",
                "检查约束验证数据有效性"
            ]
        }
    
    def _generate_api_design(self, requirements: Dict, user_stories: List) -> Dict[str, Any]:
        """生成API设计"""
        
        # 从用户故事中提取API需求
        api_endpoints = self._extract_api_endpoints(user_stories)
        
        return {
            "api_style": "RESTful API",
            "data_format": "JSON",
            "authentication": "JWT Token",
            "version_control": "URL路径版本控制 (/api/v1/)",
            "endpoints": api_endpoints,
            "error_handling": {
                "format": "统一错误响应格式",
                "codes": ["400 Bad Request", "401 Unauthorized", "403 Forbidden", "404 Not Found", "500 Internal Server Error"]
            },
            "documentation": "Swagger/OpenAPI 3.0"
        }
    
    def _generate_module_design(self, requirements: Dict, user_stories: List) -> List[Dict[str, Any]]:
        """生成模块设计"""
        
        # 从需求中识别业务模块
        modules = []
        
        functional_requirements = requirements.get("functional_requirements", [])
        
        # 按功能领域分组
        module_groups = {}
        for req in functional_requirements:
            category = req.get("category", "通用模块")
            if category not in module_groups:
                module_groups[category] = []
            module_groups[category].append(req)
        
        for module_name, reqs in module_groups.items():
            modules.append({
                "name": f"{module_name}Module",
                "description": f"{module_name}相关功能模块",
                "responsibilities": [req.get("title", "") for req in reqs],
                "components": [
                    f"{module_name}Controller",
                    f"{module_name}Service", 
                    f"{module_name}Repository"
                ],
                "interfaces": [
                    f"{module_name}Service接口",
                    f"{module_name}Repository接口"
                ]
            })
        
        return modules
    
    def _generate_technology_stack(self, architecture: Dict, context: Dict) -> Dict[str, List[str]]:
        """生成技术栈"""
        
        recommended_stack = architecture.get("technology_stack", {})
        
        return {
            "backend": recommended_stack.get("backend", [
                "Spring Boot 2.7.8",
                "Spring Security 5.7",
                "Spring Data JPA 2.7",
                "MySQL 8.0"
            ]),
            "frontend": recommended_stack.get("frontend", [
                "Vue.js 3.2",
                "Element Plus",
                "Axios",
                "Vue Router 4"
            ]),
            "database": recommended_stack.get("database", [
                "MySQL 8.0",
                "Redis 6.0"
            ]),
            "tools": recommended_stack.get("tools", [
                "Maven 3.8",
                "Docker",
                "Git",
                "Swagger 3.0"
            ]),
            "cloud": recommended_stack.get("cloud", [
                "阿里云ECS",
                "阿里云RDS",
                "阿里云Redis"
            ])
        }
    
    def _generate_security_design(self, requirements: Dict) -> Dict[str, Any]:
        """生成安全设计"""
        
        return {
            "authentication": {
                "method": "JWT Token认证",
                "token_expiry": "访问令牌2小时，刷新令牌7天",
                "password_policy": "最少8位，包含大小写字母、数字、特殊字符"
            },
            "authorization": {
                "model": "RBAC基于角色的访问控制",
                "granularity": "接口级权限控制",
                "caching": "Redis缓存用户权限"
            },
            "data_protection": [
                "密码BCrypt加密存储",
                "敏感数据AES加密",
                "HTTPS传输加密",
                "数据库连接加密"
            ],
            "security_measures": [
                "输入参数验证",
                "SQL注入防护",
                "XSS攻击防护", 
                "CSRF攻击防护",
                "接口访问频率限制"
            ]
        }
    
    def _generate_deployment_design(self, architecture: Dict) -> Dict[str, Any]:
        """生成部署设计"""
        
        return {
            "deployment_architecture": {
                "load_balancer": "Nginx反向代理",
                "application_server": "Spring Boot内嵌Tomcat",
                "database": "MySQL主从复制",
                "cache": "Redis集群"
            },
            "environments": {
                "development": "本地开发环境，H2内存数据库",
                "testing": "Docker容器，MySQL测试数据库",
                "staging": "预生产环境，完整配置",
                "production": "生产环境，高可用配置"
            },
            "containerization": {
                "docker": "应用容器化部署",
                "docker_compose": "本地开发环境编排",
                "kubernetes": "生产环境容器编排"
            },
            "monitoring": {
                "application": "Spring Boot Actuator",
                "logging": "Logback + ELK Stack",
                "metrics": "Micrometer + Prometheus",
                "alerting": "Grafana告警"
            }
        }
    
    def _generate_performance_design(self, requirements: Dict) -> Dict[str, Any]:
        """生成性能设计"""
        
        non_functional = requirements.get("non_functional_requirements", [])
        performance_reqs = [req for req in non_functional if "性能" in req.get("category", "")]
        
        return {
            "performance_targets": {
                "response_time": "API接口响应时间 < 500ms",
                "throughput": "支持1000个并发用户",
                "availability": "系统可用性 > 99.9%",
                "scalability": "支持水平扩展"
            },
            "optimization_strategies": [
                "数据库索引优化",
                "Redis缓存热点数据",
                "数据库连接池优化",
                "异步处理非关键业务",
                "CDN加速静态资源",
                "数据库读写分离"
            ],
            "caching_strategy": {
                "application_cache": "Spring Cache本地缓存",
                "distributed_cache": "Redis分布式缓存",
                "cache_patterns": ["Cache-Aside", "Write-Through", "Write-Behind"]
            },
            "database_optimization": [
                "合理设计索引",
                "优化SQL查询",
                "分库分表策略",
                "连接池配置优化"
            ]
        }
    
    def _extract_entities_from_requirements(self, requirements: Dict, user_stories: List) -> List[Dict[str, Any]]:
        """从需求中提取数据实体"""
        
        entities = []
        
        # 从用户角色中提取用户实体
        user_roles = requirements.get("user_roles", [])
        if user_roles:
            entities.append({
                "name": "User",
                "description": "用户实体",
                "attributes": [
                    {"name": "id", "type": "BIGINT", "description": "用户ID"},
                    {"name": "username", "type": "VARCHAR(50)", "description": "用户名"},
                    {"name": "email", "type": "VARCHAR(100)", "description": "邮箱"},
                    {"name": "password_hash", "type": "VARCHAR(255)", "description": "密码哈希"},
                    {"name": "created_at", "type": "DATETIME", "description": "创建时间"}
                ]
            })
        
        # 从功能需求中提取其他实体
        functional_requirements = requirements.get("functional_requirements", [])
        for req in functional_requirements:
            title = req.get("title", "")
            if "角色" in title or "权限" in title:
                entities.append({
                    "name": "Role",
                    "description": "角色实体",
                    "attributes": [
                        {"name": "id", "type": "BIGINT", "description": "角色ID"},
                        {"name": "role_name", "type": "VARCHAR(50)", "description": "角色名称"},
                        {"name": "description", "type": "VARCHAR(200)", "description": "角色描述"}
                    ]
                })
        
        return entities
    
    def _generate_table_designs(self, entities: List[Dict]) -> List[Dict[str, Any]]:
        """生成表设计"""
        
        tables = []
        for entity in entities:
            table_name = entity["name"].lower() + "s"
            
            columns = []
            for attr in entity["attributes"]:
                columns.append({
                    "name": attr["name"],
                    "type": attr["type"],
                    "nullable": "NOT NULL" if attr["name"] in ["id", "created_at"] else "NULL",
                    "description": attr["description"]
                })
            
            tables.append({
                "name": table_name,
                "description": entity["description"] + "表",
                "columns": columns,
                "primary_key": "id",
                "indexes": ["id"]
            })
        
        return tables
    
    def _generate_relationships(self, entities: List[Dict]) -> List[Dict[str, str]]:
        """生成表关系"""
        
        relationships = []
        
        # 如果有用户和角色实体，生成多对多关系
        entity_names = [e["name"] for e in entities]
        if "User" in entity_names and "Role" in entity_names:
            relationships.append({
                "type": "多对多",
                "from_table": "users",
                "to_table": "roles", 
                "through_table": "user_roles",
                "description": "用户和角色的多对多关系"
            })
        
        return relationships
    
    def _generate_indexes(self, entities: List[Dict]) -> List[Dict[str, Any]]:
        """生成索引设计"""
        
        indexes = []
        for entity in entities:
            table_name = entity["name"].lower() + "s"
            
            # 为每个表添加基本索引
            indexes.append({
                "table": table_name,
                "name": f"idx_{table_name}_id",
                "columns": ["id"],
                "type": "PRIMARY KEY"
            })
            
            # 为用户表添加唯一索引
            if entity["name"] == "User":
                indexes.extend([
                    {
                        "table": table_name,
                        "name": f"uk_{table_name}_username",
                        "columns": ["username"],
                        "type": "UNIQUE"
                    },
                    {
                        "table": table_name,
                        "name": f"uk_{table_name}_email", 
                        "columns": ["email"],
                        "type": "UNIQUE"
                    }
                ])
        
        return indexes
    
    def _extract_api_endpoints(self, user_stories: List[Dict]) -> List[Dict[str, Any]]:
        """从用户故事中提取API端点"""
        
        endpoints = []
        
        for story in user_stories:
            title = story.get("title", "")
            
            # 根据用户故事推断API端点
            if "创建" in title or "添加" in title:
                endpoints.append({
                    "method": "POST",
                    "path": "/api/v1/resources",
                    "description": f"创建资源 - {title}",
                    "request_body": "JSON格式的资源数据",
                    "response": "创建成功的资源信息"
                })
            elif "查询" in title or "获取" in title:
                endpoints.append({
                    "method": "GET", 
                    "path": "/api/v1/resources/{id}",
                    "description": f"获取资源 - {title}",
                    "parameters": "资源ID",
                    "response": "资源详细信息"
                })
            elif "更新" in title or "修改" in title:
                endpoints.append({
                    "method": "PUT",
                    "path": "/api/v1/resources/{id}",
                    "description": f"更新资源 - {title}",
                    "parameters": "资源ID",
                    "request_body": "更新的资源数据",
                    "response": "更新后的资源信息"
                })
            elif "删除" in title:
                endpoints.append({
                    "method": "DELETE",
                    "path": "/api/v1/resources/{id}",
                    "description": f"删除资源 - {title}",
                    "parameters": "资源ID",
                    "response": "删除操作结果"
                })
        
        return endpoints
    
    def _generate_markdown_document(self, design_document: Dict[str, Any]) -> str:
        """生成Markdown格式的设计文档"""
        
        metadata = design_document["metadata"]
        
        markdown = f"""# {metadata["document_title"]}

## 文档信息
- **版本**: {metadata["version"]}
- **创建日期**: {metadata["created_date"]}
- **最后更新**: {metadata["last_updated"]}
- **项目名称**: {metadata["project_name"]}

## 1. 系统概述

**项目描述**: {design_document["system_overview"]["description"]}

### 1.1 项目目标
"""
        
        for objective in design_document["system_overview"]["objectives"]:
            markdown += f"- {objective}\n"
        
        markdown += f"""
### 1.2 系统范围

**包含功能**:
"""
        for item in design_document["system_overview"]["scope"]["included"]:
            markdown += f"- {item}\n"
        
        markdown += f"""
**排除功能**:
"""
        for item in design_document["system_overview"]["scope"]["excluded"]:
            markdown += f"- {item}\n"
        
        # 架构设计部分
        arch = design_document["architecture_design"]
        markdown += f"""
## 2. 架构设计

**架构模式**: {arch["architecture_pattern"]}

### 2.1 设计原则
"""
        for principle in arch["design_principles"]:
            markdown += f"- {principle}\n"
        
        markdown += """
### 2.2 系统组件
"""
        for component in arch["system_components"]:
            markdown += f"- **{component['name']}**: {component['description']}\n"
        
        # 数据库设计部分
        db = design_document["database_design"]
        markdown += f"""
## 3. 数据库设计

**数据库类型**: {db["database_type"]}
**字符集**: {db["charset"]}
**存储引擎**: {db["storage_engine"]}

### 3.1 数据表设计
"""
        
        for table in db["tables"]:
            markdown += f"""
#### {table["name"]}表
{table["description"]}

| 字段名 | 类型 | 是否为空 | 描述 |
|--------|------|----------|------|
"""
            for column in table["columns"]:
                markdown += f"| {column['name']} | {column['type']} | {column['nullable']} | {column['description']} |\n"
        
        # API设计部分
        api = design_document["api_design"]
        markdown += f"""
## 4. API设计

**API风格**: {api["api_style"]}
**数据格式**: {api["data_format"]}
**认证方式**: {api["authentication"]}
**版本控制**: {api["version_control"]}

### 4.1 接口列表
"""
        
        for endpoint in api["endpoints"]:
            markdown += f"""
#### {endpoint["description"]}
- **方法**: {endpoint["method"]}
- **路径**: {endpoint["path"]}
- **描述**: {endpoint["description"]}
"""
        
        # 模块设计部分
        markdown += """
## 5. 模块设计
"""
        
        for module in design_document["module_design"]:
            markdown += f"""
### 5.{design_document["module_design"].index(module) + 1} {module["name"]}
**描述**: {module["description"]}

**职责**:
"""
            for responsibility in module["responsibilities"]:
                markdown += f"- {responsibility}\n"
            
            markdown += """
**组件**:
"""
            for component in module["components"]:
                markdown += f"- {component}\n"
        
        # 技术栈部分
        tech = design_document["technology_stack"]
        markdown += """
## 6. 技术栈

### 6.1 后端技术
"""
        for item in tech["backend"]:
            markdown += f"- {item}\n"
        
        markdown += """
### 6.2 前端技术
"""
        for item in tech["frontend"]:
            markdown += f"- {item}\n"
        
        markdown += """
### 6.3 数据库
"""
        for item in tech["database"]:
            markdown += f"- {item}\n"
        
        # 安全设计部分
        security = design_document["security_design"]
        markdown += f"""
## 7. 安全设计

### 7.1 认证机制
- **认证方式**: {security["authentication"]["method"]}
- **令牌过期**: {security["authentication"]["token_expiry"]}
- **密码策略**: {security["authentication"]["password_policy"]}

### 7.2 授权机制
- **授权模型**: {security["authorization"]["model"]}
- **权限粒度**: {security["authorization"]["granularity"]}
- **权限缓存**: {security["authorization"]["caching"]}

### 7.3 数据保护
"""
        for item in security["data_protection"]:
            markdown += f"- {item}\n"
        
        markdown += """
### 7.4 安全措施
"""
        for item in security["security_measures"]:
            markdown += f"- {item}\n"
        
        # 部署设计部分
        deployment = design_document["deployment_design"]
        markdown += """
## 8. 部署设计

### 8.1 部署架构
"""
        for key, value in deployment["deployment_architecture"].items():
            markdown += f"- **{key}**: {value}\n"
        
        markdown += """
### 8.2 环境配置
"""
        for env, desc in deployment["environments"].items():
            markdown += f"- **{env}**: {desc}\n"
        
        # 性能设计部分
        performance = design_document["performance_design"]
        markdown += """
## 9. 性能设计

### 9.1 性能指标
"""
        for key, value in performance["performance_targets"].items():
            markdown += f"- **{key}**: {value}\n"
        
        markdown += """
### 9.2 优化策略
"""
        for strategy in performance["optimization_strategies"]:
            markdown += f"- {strategy}\n"
        
        return markdown
    
    def save_design_document(self, design_document: Dict[str, Any], 
                           output_path: str = None) -> Dict[str, Any]:
        """保存设计文档到文件"""
        
        try:
            if not output_path:
                project_name = design_document["metadata"]["project_name"]
                output_path = f"docs/{project_name}技术设计文档.md"
            
            # 确保目录存在
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # 保存Markdown文档
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(design_document["markdown_content"])
            
            return {
                "success": True,
                "file_path": output_path,
                "message": f"设计文档已保存到: {output_path}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"保存设计文档失败: {str(e)}"
            }

# MCP Server 主函数
def main():
    """MCP Server 主入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python 设计文档生成MCP工具.py <input_data_json>")
        print("输入数据格式:")
        print(json.dumps({
            "requirements_analysis": "需求分析结果",
            "user_stories": "用户故事列表",
            "architecture_design": "架构设计结果",
            "project_context": "项目上下文信息"
        }, indent=2, ensure_ascii=False))
        sys.exit(1)
    
    input_data_json = sys.argv[1]
    
    try:
        input_data = json.loads(input_data_json)
    except json.JSONDecodeError:
        print("Invalid input JSON format")
        sys.exit(1)
    
    generator = DesignDocumentGenerator()
    
    # 生成设计文档
    result = generator.generate_design_document(input_data)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
