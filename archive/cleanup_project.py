#!/usr/bin/env python3
"""
项目清理脚本
自动清理不需要的文件，保持项目整洁
"""

import os
import shutil
from pathlib import Path
import json

class ProjectCleaner:
    def __init__(self, project_root="."):
        self.project_root = Path(project_root)
        self.deleted_files = []
        self.deleted_dirs = []
        self.kept_files = []
        
    def backup_important_files(self):
        """备份重要文件"""
        print("📦 创建备份...")
        backup_dir = self.project_root / "backup_before_cleanup"
        backup_dir.mkdir(exist_ok=True)
        
        # 备份配置文件
        important_files = [
            "claude_desktop_mcp_config.json",
            "config/完整MCP配置.json"
        ]
        
        for file_path in important_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                backup_path = backup_dir / file_path
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(full_path, backup_path)
                print(f"  ✅ 已备份: {file_path}")
        
        return backup_dir
    
    def clean_temporary_scripts(self):
        """清理临时脚本"""
        print("\n🧹 清理临时脚本...")
        
        temp_scripts = [
            "check_mcp_config.py",
            "complete_mcp_fix.py", 
            "create_real_mcp_server.py",
            "fix_all_mcp_tools.py",
            "智能包名配置工具.py"
        ]
        
        for script in temp_scripts:
            file_path = self.project_root / script
            if file_path.exists():
                file_path.unlink()
                self.deleted_files.append(script)
                print(f"  ❌ 已删除: {script}")
    
    def clean_test_files(self):
        """清理测试文件"""
        print("\n🧹 清理测试文件...")
        
        test_files = [
            "test_mcp_tools.py",
            "test_mcp_functionality.py"
        ]
        
        for test_file in test_files:
            file_path = self.project_root / test_file
            if file_path.exists():
                file_path.unlink()
                self.deleted_files.append(test_file)
                print(f"  ❌ 已删除: {test_file}")
    
    def clean_generated_files(self):
        """清理生成的文件"""
        print("\n🧹 清理生成的文件...")
        
        # 删除 generated 目录
        generated_dir = self.project_root / "generated"
        if generated_dir.exists():
            shutil.rmtree(generated_dir)
            self.deleted_dirs.append("generated/")
            print(f"  ❌ 已删除目录: generated/")
        
        # 删除 test-examples 目录
        test_examples_dir = self.project_root / "test-examples"
        if test_examples_dir.exists():
            shutil.rmtree(test_examples_dir)
            self.deleted_dirs.append("test-examples/")
            print(f"  ❌ 已删除目录: test-examples/")
        
        # 删除 package_config.json
        package_config = self.project_root / "package_config.json"
        if package_config.exists():
            package_config.unlink()
            self.deleted_files.append("package_config.json")
            print(f"  ❌ 已删除: package_config.json")
    
    def clean_old_mcp_tools(self):
        """清理旧版本的 MCP 工具"""
        print("\n🧹 清理旧版本 MCP 工具...")
        
        mcp_tools_dir = self.project_root / "mcp-tools"
        if not mcp_tools_dir.exists():
            return
        
        # 定义每个目录中要保留的文件
        keep_files = {
            "01-requirements": ["标准需求分析MCP服务器.py"],
            "02-design": ["标准设计文档MCP服务器.py"],
            "03-architecture": ["标准架构分析MCP服务器.py"],
            "04-generation": ["标准代码生成MCP服务器.py"],
            "05-testing": ["标准测试生成MCP服务器.py", "标准文档生成MCP服务器.py"]
        }
        
        for subdir, keep_list in keep_files.items():
            subdir_path = mcp_tools_dir / subdir
            if subdir_path.exists():
                for file_path in subdir_path.iterdir():
                    if file_path.is_file() and file_path.name not in keep_list:
                        if not file_path.name.startswith('.'):  # 不删除隐藏文件
                            file_path.unlink()
                            relative_path = f"mcp-tools/{subdir}/{file_path.name}"
                            self.deleted_files.append(relative_path)
                            print(f"  ❌ 已删除: {relative_path}")
    
    def clean_cache_files(self):
        """清理缓存文件"""
        print("\n🧹 清理缓存文件...")
        
        # 删除 __pycache__ 目录
        for root, dirs, files in os.walk(self.project_root):
            for dir_name in dirs[:]:  # 使用切片复制避免修改正在迭代的列表
                if dir_name == "__pycache__":
                    cache_path = Path(root) / dir_name
                    shutil.rmtree(cache_path)
                    relative_path = cache_path.relative_to(self.project_root)
                    self.deleted_dirs.append(str(relative_path) + "/")
                    print(f"  ❌ 已删除缓存: {relative_path}/")
                    dirs.remove(dir_name)  # 从迭代中移除
    
    def clean_redundant_configs(self):
        """清理冗余配置文件"""
        print("\n🧹 清理冗余配置...")
        
        # 保留自动生成的配置，删除旧的硬编码配置
        old_config = self.project_root / "config" / "完整MCP配置.json"
        new_config = self.project_root / "claude_desktop_mcp_config.json"
        
        if old_config.exists() and new_config.exists():
            old_config.unlink()
            self.deleted_files.append("config/完整MCP配置.json")
            print(f"  ❌ 已删除旧配置: config/完整MCP配置.json")
            print(f"  ✅ 保留新配置: claude_desktop_mcp_config.json")
    
    def clean_redundant_docs(self):
        """清理冗余文档"""
        print("\n🧹 清理冗余文档...")
        
        redundant_docs = [
            "MCP工具修复报告.md",
            "文件结构说明.md", 
            "项目状态总结.md"
        ]
        
        for doc in redundant_docs:
            doc_path = self.project_root / doc
            if doc_path.exists():
                doc_path.unlink()
                self.deleted_files.append(doc)
                print(f"  ❌ 已删除文档: {doc}")
    
    def generate_cleanup_report(self):
        """生成清理报告"""
        print("\n📊 生成清理报告...")
        
        report = {
            "cleanup_summary": {
                "deleted_files_count": len(self.deleted_files),
                "deleted_dirs_count": len(self.deleted_dirs),
                "total_deleted": len(self.deleted_files) + len(self.deleted_dirs)
            },
            "deleted_files": self.deleted_files,
            "deleted_directories": self.deleted_dirs,
            "remaining_core_files": [
                "README.md",
                "claude_desktop_mcp_config.json",
                "generate_mcp_config.py",
                "Claude_Desktop_MCP配置指南.md",
                "MCP工具测试报告.md",
                "simple-mcp-server说明.md",
                "mcp-tools/simple-mcp-server.py",
                "mcp-tools/01-requirements/标准需求分析MCP服务器.py",
                "mcp-tools/02-design/标准设计文档MCP服务器.py",
                "mcp-tools/03-architecture/标准架构分析MCP服务器.py",
                "mcp-tools/04-generation/标准代码生成MCP服务器.py",
                "mcp-tools/05-testing/标准测试生成MCP服务器.py",
                "mcp-tools/05-testing/标准文档生成MCP服务器.py"
            ]
        }
        
        report_file = self.project_root / "cleanup_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ 清理报告已保存: cleanup_report.json")
        return report
    
    def run_cleanup(self, confirm=True):
        """执行清理"""
        print("🚀 开始项目清理...")
        print("=" * 50)
        
        if confirm:
            response = input("⚠️  确定要执行清理吗？这将删除多个文件！(y/n): ")
            if response.lower() not in ['y', 'yes', '是']:
                print("❌ 清理已取消")
                return
        
        # 备份重要文件
        backup_dir = self.backup_important_files()
        
        # 执行各种清理
        self.clean_temporary_scripts()
        self.clean_test_files()
        self.clean_generated_files()
        self.clean_old_mcp_tools()
        self.clean_cache_files()
        self.clean_redundant_configs()
        self.clean_redundant_docs()
        
        # 生成报告
        report = self.generate_cleanup_report()
        
        print("\n" + "=" * 50)
        print("🎉 清理完成！")
        print(f"📊 删除了 {report['cleanup_summary']['total_deleted']} 个文件/目录")
        print(f"📦 备份位置: {backup_dir}")
        print(f"📋 详细报告: cleanup_report.json")
        
        print("\n✅ 建议下一步:")
        print("1. 测试 MCP 工具是否正常工作")
        print("2. 检查 claude_desktop_mcp_config.json 配置")
        print("3. 如有问题，可从备份目录恢复文件")

def main():
    """主函数"""
    cleaner = ProjectCleaner()
    cleaner.run_cleanup()

if __name__ == "__main__":
    main()
