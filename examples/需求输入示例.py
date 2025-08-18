#!/usr/bin/env python3
"""
需求输入示例脚本
演示如何使用不同方式输入产品需求
"""

import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'mcp-tools', '01-requirements'))

from 需求文档解析MCP工具 import RequirementsDocumentParser

def example_codesign_url():
    """示例：CodeSign链接解析"""
    print("=== CodeSign链接解析示例 ===")
    
    parser = RequirementsDocumentParser()
    
    # 模拟CodeSign链接输入
    input_data = {
        "type": "codesign_url",
        "content": "https://codesign.qq.com/s/example123"  # 示例链接
    }
    
    print(f"输入数据: {json.dumps(input_data, ensure_ascii=False, indent=2)}")
    
    result = parser.parse_requirements_input(input_data)
    print(f"解析结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    print()

def example_screenshot_folder():
    """示例：截图文件夹解析"""
    print("=== 截图文件夹解析示例 ===")
    
    parser = RequirementsDocumentParser()
    
    # 创建示例截图文件夹（如果不存在）
    screenshot_folder = "./examples/screenshots"
    os.makedirs(screenshot_folder, exist_ok=True)
    
    input_data = {
        "type": "screenshot_folder",
        "content": screenshot_folder
    }
    
    print(f"输入数据: {json.dumps(input_data, ensure_ascii=False, indent=2)}")
    
    result = parser.parse_requirements_input(input_data)
    print(f"解析结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    print()

def example_document_file():
    """示例：文档文件解析"""
    print("=== 文档文件解析示例 ===")
    
    parser = RequirementsDocumentParser()
    
    # 创建示例需求文档
    doc_content = """# 用户管理系统需求文档

## 1. 项目概述
开发一个用户管理系统，支持用户注册、登录、个人信息管理等功能。

## 2. 功能需求

### 2.1 用户注册
- 用户可以通过邮箱注册账号
- 注册时需要验证邮箱有效性
- 密码需要符合安全规范

### 2.2 用户登录
- 支持邮箱和用户名登录
- 支持记住登录状态
- 登录失败3次后锁定账号

### 2.3 个人信息管理
- 用户可以查看和修改个人信息
- 支持头像上传
- 支持密码修改

## 3. 非功能需求

### 3.1 性能要求
- 页面响应时间不超过2秒
- 支持1000个并发用户

### 3.2 安全要求
- 密码需要加密存储
- 支持HTTPS访问
- 实现访问控制

## 4. 用户角色
- 普通用户：可以管理自己的信息
- 管理员：可以管理所有用户信息
- 系统管理员：拥有系统配置权限
"""
    
    # 创建示例文档文件
    doc_file = "./examples/用户管理系统需求.md"
    os.makedirs("./examples", exist_ok=True)
    
    with open(doc_file, 'w', encoding='utf-8') as f:
        f.write(doc_content)
    
    input_data = {
        "type": "document_file",
        "content": doc_file
    }
    
    print(f"输入数据: {json.dumps(input_data, ensure_ascii=False, indent=2)}")
    
    result = parser.parse_requirements_input(input_data)
    print(f"解析结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    print()

def example_direct_text():
    """示例：直接文本输入"""
    print("=== 直接文本输入示例 ===")
    
    parser = RequirementsDocumentParser()
    
    requirements_text = """
    我要开发一个电商订单管理系统，主要功能包括：
    
    1. 订单创建：客户可以创建新订单，选择商品和数量
    2. 订单查询：客户和管理员都可以查询订单状态
    3. 订单处理：管理员可以处理订单，更新订单状态
    4. 支付集成：支持多种支付方式，如支付宝、微信支付
    5. 库存管理：自动更新商品库存，防止超卖
    
    非功能需求：
    - 系统要支持高并发，至少1000个用户同时访问
    - 响应时间要在3秒以内
    - 数据要加密存储，确保安全性
    - 要有完整的日志记录和监控
    
    用户角色：
    - 客户：可以创建和查询自己的订单
    - 商家：可以管理商品和处理订单
    - 管理员：拥有系统管理权限
    - 财务：可以查看财务相关数据
    """
    
    input_data = {
        "type": "direct_text",
        "content": requirements_text.strip()
    }
    
    print(f"输入数据: {json.dumps(input_data, ensure_ascii=False, indent=2)}")
    
    result = parser.parse_requirements_input(input_data)
    print(f"解析结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    print()

def example_validation():
    """示例：输入验证"""
    print("=== 输入验证示例 ===")
    
    parser = RequirementsDocumentParser()
    
    # 测试无效输入
    invalid_inputs = [
        {},  # 缺少字段
        {"type": "invalid_type"},  # 无效类型
        {"type": "direct_text"},  # 缺少content
        {"type": "direct_text", "content": ""}  # 空内容
    ]
    
    for i, input_data in enumerate(invalid_inputs):
        print(f"测试无效输入 {i+1}: {json.dumps(input_data, ensure_ascii=False)}")
        
        validation_result = parser.validate_input(input_data)
        print(f"验证结果: {json.dumps(validation_result, ensure_ascii=False, indent=2)}")
        print()

def show_supported_formats():
    """显示支持的格式"""
    print("=== 支持的输入格式 ===")
    
    parser = RequirementsDocumentParser()
    formats = parser.get_supported_formats()
    
    print(json.dumps(formats, ensure_ascii=False, indent=2))
    print()

def main():
    """主函数"""
    print("🚀 需求输入方式示例演示")
    print("=" * 50)
    
    # 显示支持的格式
    show_supported_formats()
    
    # 运行各种示例
    example_direct_text()
    example_document_file()
    example_screenshot_folder()
    # example_codesign_url()  # 需要真实链接才能测试
    
    # 输入验证示例
    example_validation()
    
    print("✅ 所有示例演示完成！")
    print("\n📋 使用建议：")
    print("1. 对于在线需求文档，推荐使用CodeSign链接方式")
    print("2. 对于截图形式的需求，使用截图文件夹方式")
    print("3. 对于本地文档，推荐Markdown格式")
    print("4. 对于简单需求，可以直接文本输入")

if __name__ == "__main__":
    main()
