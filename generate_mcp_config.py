#!/usr/bin/env python3
"""
MCP 配置生成器
自动生成适合当前环境的 Claude Desktop MCP 配置
"""

import json
import os
import sys
from pathlib import Path

def get_current_project_path():
    """获取当前项目的绝对路径"""
    return Path(__file__).parent.absolute()

def generate_mcp_config(project_path=None):
    """生成 MCP 配置"""
    if project_path is None:
        project_path = get_current_project_path()
    
    # 确保路径使用正确的分隔符
    if os.name == 'nt':  # Windows
        path_str = str(project_path).replace('\\', '\\\\')
    else:  # Unix-like
        path_str = str(project_path)
    
    config = {
        "mcpServers": {
            "requirements-analyzer": {
                "command": "python",
                "args": [
                    f"{path_str}\\mcp-tools\\01-requirements\\标准需求分析MCP服务器.py" if os.name == 'nt' 
                    else f"{path_str}/mcp-tools/01-requirements/标准需求分析MCP服务器.py"
                ],
                "description": "需求分析工具 - 分析产品需求，生成技术规格"
            },
            "design-generator": {
                "command": "python",
                "args": [
                    f"{path_str}\\mcp-tools\\02-design\\标准设计文档MCP服务器.py" if os.name == 'nt'
                    else f"{path_str}/mcp-tools/02-design/标准设计文档MCP服务器.py"
                ],
                "description": "设计文档生成工具 - 生成设计文档和API设计"
            },
            "architecture-analyzer": {
                "command": "python",
                "args": [
                    f"{path_str}\\mcp-tools\\03-architecture\\标准架构分析MCP服务器.py" if os.name == 'nt'
                    else f"{path_str}/mcp-tools/03-architecture/标准架构分析MCP服务器.py"
                ],
                "description": "架构分析工具 - 分析项目架构模式"
            },
            "code-generator": {
                "command": "python",
                "args": [
                    f"{path_str}\\mcp-tools\\04-generation\\标准代码生成MCP服务器.py" if os.name == 'nt'
                    else f"{path_str}/mcp-tools/04-generation/标准代码生成MCP服务器.py"
                ],
                "description": "代码生成工具 - 生成完整的CRUD模块"
            },
            "test-generator": {
                "command": "python",
                "args": [
                    f"{path_str}\\mcp-tools\\05-testing\\标准测试生成MCP服务器.py" if os.name == 'nt'
                    else f"{path_str}/mcp-tools/05-testing/标准测试生成MCP服务器.py"
                ],
                "description": "测试生成工具 - 生成单元测试和集成测试"
            },
            "documentation-generator": {
                "command": "python",
                "args": [
                    f"{path_str}\\mcp-tools\\05-testing\\标准文档生成MCP服务器.py" if os.name == 'nt'
                    else f"{path_str}/mcp-tools/05-testing/标准文档生成MCP服务器.py"
                ],
                "description": "文档生成工具 - 生成API文档和README"
            }
        }
    }
    
    return config

def get_claude_desktop_config_path():
    """获取 Claude Desktop 配置文件路径"""
    if os.name == 'nt':  # Windows
        return Path(os.environ['APPDATA']) / 'Claude' / 'claude_desktop_config.json'
    elif sys.platform == 'darwin':  # macOS
        return Path.home() / 'Library' / 'Application Support' / 'Claude' / 'claude_desktop_config.json'
    else:  # Linux
        return Path.home() / '.config' / 'Claude' / 'claude_desktop_config.json'

def verify_mcp_tools():
    """验证 MCP 工具文件是否存在"""
    project_path = get_current_project_path()
    mcp_tools_path = project_path / 'mcp-tools'
    
    if not mcp_tools_path.exists():
        return False, f"MCP 工具目录不存在: {mcp_tools_path}"
    
    required_files = [
        "01-requirements/标准需求分析MCP服务器.py",
        "02-design/标准设计文档MCP服务器.py", 
        "03-architecture/标准架构分析MCP服务器.py",
        "04-generation/标准代码生成MCP服务器.py",
        "05-testing/标准测试生成MCP服务器.py",
        "05-testing/标准文档生成MCP服务器.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = mcp_tools_path / file_path
        if not full_path.exists():
            missing_files.append(file_path)
    
    if missing_files:
        return False, f"缺少文件: {missing_files}"
    
    return True, "所有 MCP 工具文件都存在"

def main():
    """主函数"""
    print("MCP 配置生成器")
    print("=" * 50)
    
    # 验证 MCP 工具
    print("1. 验证 MCP 工具文件...")
    valid, message = verify_mcp_tools()
    if not valid:
        print(f"❌ {message}")
        return
    print(f"✅ {message}")
    
    # 获取项目路径
    project_path = get_current_project_path()
    print(f"2. 项目路径: {project_path}")
    
    # 生成配置
    print("3. 生成 MCP 配置...")
    config = generate_mcp_config(project_path)
    
    # 保存到本地文件
    output_file = project_path / "claude_desktop_mcp_config.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"✅ 配置已保存到: {output_file}")
    
    # 显示 Claude Desktop 配置路径
    claude_config_path = get_claude_desktop_config_path()
    print(f"\n4. Claude Desktop 配置文件路径:")
    print(f"   {claude_config_path}")
    
    # 检查 Claude Desktop 配置文件是否存在
    if claude_config_path.exists():
        print("✅ Claude Desktop 配置文件存在")
        
        # 询问是否自动更新
        response = input("\n是否要自动更新 Claude Desktop 配置？(y/n): ")
        if response.lower() in ['y', 'yes', '是']:
            try:
                # 读取现有配置
                with open(claude_config_path, 'r', encoding='utf-8') as f:
                    existing_config = json.load(f)
                
                # 备份现有配置
                backup_path = claude_config_path.with_suffix('.json.backup')
                with open(backup_path, 'w', encoding='utf-8') as f:
                    json.dump(existing_config, f, indent=2, ensure_ascii=False)
                print(f"✅ 已备份现有配置到: {backup_path}")
                
                # 合并配置
                if "mcpServers" not in existing_config:
                    existing_config["mcpServers"] = {}
                
                existing_config["mcpServers"].update(config["mcpServers"])
                
                # 保存更新后的配置
                with open(claude_config_path, 'w', encoding='utf-8') as f:
                    json.dump(existing_config, f, indent=2, ensure_ascii=False)
                
                print("✅ Claude Desktop 配置已更新")
                print("⚠️  请重启 Claude Desktop 以加载新配置")
                
            except Exception as e:
                print(f"❌ 更新配置失败: {e}")
                print("请手动复制配置内容")
        else:
            print("请手动将生成的配置添加到 Claude Desktop 配置文件中")
    else:
        print("⚠️  Claude Desktop 配置文件不存在")
        print("请先运行 Claude Desktop，然后手动创建配置文件")
    
    print(f"\n5. 使用说明:")
    print("   - 重启 Claude Desktop")
    print("   - 在对话中询问：'你现在有哪些 MCP 工具可用？'")
    print("   - 开始使用各种开发工具！")
    
    print(f"\n🎉 配置生成完成！")

if __name__ == "__main__":
    main()
