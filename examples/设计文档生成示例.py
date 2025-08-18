#!/usr/bin/env python3
"""
设计文档生成示例脚本
演示如何从需求分析结果生成完整的技术设计文档
"""

import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'mcp-tools', '02-design'))

from 设计文档生成MCP工具 import DesignDocumentGenerator

def create_sample_requirements_analysis():
    """创建示例需求分析结果"""
    return {
        "project_description": "用户管理系统，提供用户注册、登录、个人信息管理、权限控制等功能",
        "functional_requirements": [
            {
                "id": "FR001",
                "title": "用户注册",
                "description": "用户可以通过邮箱注册账号",
                "category": "用户管理",
                "priority": "高"
            },
            {
                "id": "FR002", 
                "title": "用户登录",
                "description": "用户可以通过用户名或邮箱登录系统",
                "category": "用户管理",
                "priority": "高"
            },
            {
                "id": "FR003",
                "title": "个人信息管理",
                "description": "用户可以查看和修改个人信息",
                "category": "用户管理",
                "priority": "中"
            },
            {
                "id": "FR004",
                "title": "角色管理",
                "description": "管理员可以创建和管理用户角色",
                "category": "权限管理",
                "priority": "中"
            },
            {
                "id": "FR005",
                "title": "权限分配",
                "description": "管理员可以为角色分配权限",
                "category": "权限管理",
                "priority": "中"
            }
        ],
        "non_functional_requirements": [
            {
                "id": "NFR001",
                "title": "性能要求",
                "description": "系统响应时间不超过2秒",
                "category": "性能",
                "priority": "高"
            },
            {
                "id": "NFR002",
                "title": "并发要求",
                "description": "支持1000个并发用户",
                "category": "性能",
                "priority": "高"
            },
            {
                "id": "NFR003",
                "title": "安全要求",
                "description": "密码需要加密存储，支持HTTPS访问",
                "category": "安全",
                "priority": "高"
            }
        ],
        "user_roles": [
            {
                "name": "普通用户",
                "description": "可以管理自己的个人信息"
            },
            {
                "name": "管理员",
                "description": "可以管理所有用户和角色权限"
            },
            {
                "name": "系统管理员",
                "description": "拥有系统配置和维护权限"
            }
        ],
        "business_rules": [
            "用户名必须唯一",
            "邮箱必须唯一且有效",
            "密码长度至少8位",
            "用户登录失败3次后锁定账号"
        ]
    }

def create_sample_user_stories():
    """创建示例用户故事"""
    return [
        {
            "id": "US001",
            "title": "用户注册",
            "description": "作为一个新用户，我希望能够注册账号，以便使用系统功能",
            "acceptance_criteria": [
                "用户可以输入用户名、邮箱和密码",
                "系统验证邮箱格式和用户名唯一性",
                "注册成功后发送确认邮件"
            ],
            "story_points": 5,
            "priority": "高"
        },
        {
            "id": "US002",
            "title": "用户登录",
            "description": "作为一个注册用户，我希望能够登录系统，以便访问个人功能",
            "acceptance_criteria": [
                "用户可以使用用户名或邮箱登录",
                "系统验证用户凭据",
                "登录成功后跳转到主页"
            ],
            "story_points": 3,
            "priority": "高"
        },
        {
            "id": "US003",
            "title": "个人信息管理",
            "description": "作为一个登录用户，我希望能够查看和修改个人信息",
            "acceptance_criteria": [
                "用户可以查看个人资料",
                "用户可以修改姓名、邮箱等信息",
                "修改后需要重新验证邮箱"
            ],
            "story_points": 3,
            "priority": "中"
        },
        {
            "id": "US004",
            "title": "角色管理",
            "description": "作为管理员，我希望能够创建和管理用户角色",
            "acceptance_criteria": [
                "管理员可以创建新角色",
                "管理员可以编辑角色信息",
                "管理员可以删除未使用的角色"
            ],
            "story_points": 5,
            "priority": "中"
        }
    ]

def create_sample_architecture_design():
    """创建示例架构设计"""
    return {
        "architecture_pattern": "分层架构",
        "components": [
            {
                "name": "表现层",
                "description": "Spring MVC Controllers，处理HTTP请求和响应"
            },
            {
                "name": "业务逻辑层", 
                "description": "Service层，实现业务规则和流程控制"
            },
            {
                "name": "数据访问层",
                "description": "Repository层，封装数据访问逻辑"
            },
            {
                "name": "数据库层",
                "description": "MySQL数据库，数据持久化存储"
            }
        ],
        "technology_stack": {
            "backend": [
                "Spring Boot 2.7.8",
                "Spring Security 5.7",
                "Spring Data JPA 2.7",
                "MySQL 8.0"
            ],
            "frontend": [
                "Vue.js 3.2",
                "Element Plus",
                "Axios",
                "Vue Router 4"
            ],
            "database": [
                "MySQL 8.0",
                "Redis 6.0"
            ],
            "tools": [
                "Maven 3.8",
                "Docker",
                "Git",
                "Swagger 3.0"
            ]
        }
    }

def create_sample_project_context():
    """创建示例项目上下文"""
    return {
        "project_name": "用户管理系统",
        "team_size": 5,
        "development_timeline": "3个月",
        "target_environment": "云服务器部署"
    }

def example_generate_design_document():
    """示例：生成设计文档"""
    print("=== 设计文档生成示例 ===")
    
    generator = DesignDocumentGenerator()
    
    # 准备输入数据
    input_data = {
        "requirements_analysis": create_sample_requirements_analysis(),
        "user_stories": create_sample_user_stories(),
        "architecture_design": create_sample_architecture_design(),
        "project_context": create_sample_project_context()
    }
    
    print("输入数据准备完成...")
    print(f"- 功能需求: {len(input_data['requirements_analysis']['functional_requirements'])}个")
    print(f"- 非功能需求: {len(input_data['requirements_analysis']['non_functional_requirements'])}个")
    print(f"- 用户故事: {len(input_data['user_stories'])}个")
    print(f"- 用户角色: {len(input_data['requirements_analysis']['user_roles'])}个")
    print()
    
    # 生成设计文档
    result = generator.generate_design_document(input_data)
    
    if result.get("success"):
        print("✅ 设计文档生成成功！")
        print()
        
        design_doc = result["design_document"]
        
        # 显示文档概要
        print("📋 文档概要:")
        metadata = design_doc["metadata"]
        print(f"- 文档标题: {metadata['document_title']}")
        print(f"- 项目名称: {metadata['project_name']}")
        print(f"- 创建日期: {metadata['created_date']}")
        print()
        
        # 显示系统概述
        print("🏗️ 系统概述:")
        overview = design_doc["system_overview"]
        print(f"- 项目描述: {overview['description'][:100]}...")
        print(f"- 功能目标: {len(overview['objectives'])}个")
        print(f"- 用户角色: {len(overview['stakeholders'])}个")
        print()
        
        # 显示架构设计
        print("🏛️ 架构设计:")
        arch = design_doc["architecture_design"]
        print(f"- 架构模式: {arch['architecture_pattern']}")
        print(f"- 系统组件: {len(arch['system_components'])}个")
        print(f"- 设计原则: {len(arch['design_principles'])}个")
        print()
        
        # 显示数据库设计
        print("🗄️ 数据库设计:")
        db = design_doc["database_design"]
        print(f"- 数据库类型: {db['database_type']}")
        print(f"- 数据实体: {len(db['entities'])}个")
        print(f"- 数据表: {len(db['tables'])}个")
        print()
        
        # 显示API设计
        print("🔌 API设计:")
        api = design_doc["api_design"]
        print(f"- API风格: {api['api_style']}")
        print(f"- 数据格式: {api['data_format']}")
        print(f"- 认证方式: {api['authentication']}")
        print(f"- 接口端点: {len(api['endpoints'])}个")
        print()
        
        # 显示模块设计
        print("📦 模块设计:")
        modules = design_doc["module_design"]
        print(f"- 业务模块: {len(modules)}个")
        for module in modules:
            print(f"  - {module['name']}: {module['description']}")
        print()
        
        # 显示技术栈
        print("⚙️ 技术栈:")
        tech = design_doc["technology_stack"]
        print(f"- 后端技术: {', '.join(tech['backend'][:3])}...")
        print(f"- 前端技术: {', '.join(tech['frontend'][:3])}...")
        print(f"- 数据库: {', '.join(tech['database'])}")
        print()
        
        # 保存文档到文件
        save_result = generator.save_design_document(result, "./examples/生成的用户管理系统设计文档.md")
        
        if save_result.get("success"):
            print(f"📄 设计文档已保存到: {save_result['file_path']}")
            print()
            
            # 显示部分Markdown内容
            markdown_lines = result["markdown_content"].split('\n')
            print("📝 Markdown文档预览（前20行）:")
            print("-" * 50)
            for i, line in enumerate(markdown_lines[:20]):
                print(f"{i+1:2d}: {line}")
            print("...")
            print(f"总共 {len(markdown_lines)} 行")
        else:
            print(f"❌ 保存文档失败: {save_result.get('error')}")
    else:
        print(f"❌ 生成设计文档失败: {result.get('error')}")

def example_markdown_structure():
    """示例：显示生成的Markdown文档结构"""
    print("=== 生成的设计文档结构 ===")
    
    structure = """
# 用户管理系统技术设计文档

## 文档信息
- 版本、创建日期、项目信息

## 1. 系统概述
- 项目描述和目标
- 系统范围和功能
- 利益相关者

## 2. 架构设计
- 架构模式和设计原则
- 系统组件和层次结构
- 通信模式

## 3. 数据库设计
- 数据库类型和配置
- 数据表设计
- 索引和约束

## 4. API设计
- API风格和认证
- 接口端点列表
- 错误处理机制

## 5. 模块设计
- 业务模块划分
- 组件职责定义
- 接口设计

## 6. 技术栈
- 后端、前端、数据库技术
- 开发工具和部署方案

## 7. 安全设计
- 认证和授权机制
- 数据保护措施
- 安全防护策略

## 8. 部署设计
- 部署架构和环境配置
- 容器化和监控方案

## 9. 性能设计
- 性能指标和优化策略
- 缓存和数据库优化
    """
    
    print(structure)
    print()
    print("✅ 这个结构涵盖了完整的技术设计文档内容")
    print("✅ 可以直接用于团队技术评审")
    print("✅ 可以作为后续开发的技术依据")
    print("✅ 支持版本控制和文档维护")

def main():
    """主函数"""
    print("🚀 设计文档生成示例演示")
    print("=" * 50)
    
    # 生成设计文档示例
    example_generate_design_document()
    
    print("\n" + "=" * 50)
    
    # 显示文档结构
    example_markdown_structure()
    
    print("\n✅ 示例演示完成！")
    print("\n📋 使用建议：")
    print("1. 从产品需求开始，先生成技术设计文档")
    print("2. 团队评审设计文档，确认技术方案")
    print("3. 基于设计文档进行代码生成和开发")
    print("4. 设计文档可以复用到其他类似项目")

if __name__ == "__main__":
    main()
