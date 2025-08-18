#!/usr/bin/env python3
"""
需求文档解析 MCP Server
支持多种需求输入方式：腾讯CodeSign链接、截图文件、文档文件等
"""

import json
import requests
import base64
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import re
from PIL import Image
import pytesseract

class RequirementsDocumentParser:
    """需求文档解析器"""
    
    def __init__(self):
        self.supported_formats = {
            "url": ["codesign", "tapd", "jira", "confluence"],
            "image": [".png", ".jpg", ".jpeg", ".bmp", ".gif"],
            "document": [".md", ".txt", ".docx", ".pdf"],
            "json": [".json"]
        }
    
    def parse_requirements_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """解析需求输入，支持多种格式"""
        
        input_type = input_data.get("type", "")
        input_content = input_data.get("content", "")
        
        if input_type == "codesign_url":
            return self._parse_codesign_url(input_content)
        elif input_type == "screenshot_folder":
            return self._parse_screenshot_folder(input_content)
        elif input_type == "document_file":
            return self._parse_document_file(input_content)
        elif input_type == "direct_text":
            return self._parse_direct_text(input_content)
        else:
            return {"error": f"不支持的输入类型: {input_type}"}
    
    def _parse_codesign_url(self, url: str) -> Dict[str, Any]:
        """解析腾讯CodeSign链接"""
        try:
            # 检查是否是CodeSign链接
            if "codesign" not in url.lower() and "tapd" not in url.lower():
                return {"error": "不是有效的CodeSign或TAPD链接"}
            
            # 尝试获取页面内容
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # 解析HTML内容
            html_content = response.text
            requirements_text = self._extract_requirements_from_html(html_content)
            
            if not requirements_text:
                return {
                    "error": "无法从链接中提取需求内容",
                    "suggestion": "请检查链接是否可访问，或者尝试复制需求内容直接输入"
                }
            
            return {
                "source": "codesign_url",
                "url": url,
                "extracted_text": requirements_text,
                "parsing_method": "html_extraction",
                "success": True
            }
            
        except requests.RequestException as e:
            return {
                "error": f"无法访问链接: {str(e)}",
                "suggestion": "请检查网络连接或链接权限，或者尝试截图方式"
            }
        except Exception as e:
            return {
                "error": f"解析链接时出错: {str(e)}",
                "suggestion": "请尝试其他输入方式"
            }
    
    def _extract_requirements_from_html(self, html_content: str) -> str:
        """从HTML中提取需求内容"""
        
        # 移除HTML标签，提取纯文本
        import re
        
        # 移除script和style标签
        html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        
        # 移除HTML标签
        text_content = re.sub(r'<[^>]+>', ' ', html_content)
        
        # 清理空白字符
        text_content = re.sub(r'\s+', ' ', text_content).strip()
        
        # 查找需求相关的关键内容
        requirement_patterns = [
            r'需求描述[：:](.*?)(?=功能|非功能|验收|$)',
            r'功能需求[：:](.*?)(?=非功能|验收|$)',
            r'业务需求[：:](.*?)(?=技术|验收|$)',
            r'产品需求[：:](.*?)(?=开发|测试|$)'
        ]
        
        extracted_requirements = []
        for pattern in requirement_patterns:
            matches = re.findall(pattern, text_content, re.IGNORECASE | re.DOTALL)
            extracted_requirements.extend(matches)
        
        if extracted_requirements:
            return ' '.join(extracted_requirements).strip()
        
        # 如果没有找到特定模式，返回清理后的全部内容（限制长度）
        if len(text_content) > 100:  # 确保有足够内容
            return text_content[:5000]  # 限制长度避免过长
        
        return ""
    
    def _parse_screenshot_folder(self, folder_path: str) -> Dict[str, Any]:
        """解析截图文件夹"""
        try:
            folder = Path(folder_path)
            if not folder.exists():
                return {"error": f"文件夹不存在: {folder_path}"}
            
            # 查找图片文件
            image_files = []
            for ext in self.supported_formats["image"]:
                image_files.extend(list(folder.glob(f"*{ext}")))
            
            if not image_files:
                return {"error": "文件夹中没有找到图片文件"}
            
            # 对图片文件排序
            image_files.sort()
            
            extracted_texts = []
            processed_files = []
            
            for image_file in image_files:
                try:
                    # 使用OCR提取文字
                    text = self._extract_text_from_image(str(image_file))
                    if text.strip():
                        extracted_texts.append({
                            "file": str(image_file),
                            "text": text.strip()
                        })
                        processed_files.append(str(image_file))
                except Exception as e:
                    print(f"处理图片 {image_file} 时出错: {e}")
                    continue
            
            if not extracted_texts:
                return {"error": "无法从图片中提取文字内容"}
            
            # 合并所有提取的文字
            combined_text = "\n\n".join([item["text"] for item in extracted_texts])
            
            return {
                "source": "screenshot_folder",
                "folder_path": folder_path,
                "processed_files": processed_files,
                "extracted_texts": extracted_texts,
                "combined_text": combined_text,
                "parsing_method": "ocr_extraction",
                "success": True
            }
            
        except Exception as e:
            return {
                "error": f"处理截图文件夹时出错: {str(e)}",
                "suggestion": "请检查文件夹路径和图片文件格式"
            }
    
    def _extract_text_from_image(self, image_path: str) -> str:
        """从图片中提取文字（OCR）"""
        try:
            # 打开图片
            image = Image.open(image_path)
            
            # 使用pytesseract进行OCR
            # 支持中文识别
            text = pytesseract.image_to_string(image, lang='chi_sim+eng')
            
            return text
            
        except Exception as e:
            # 如果OCR失败，尝试简单的文字识别
            print(f"OCR识别失败: {e}")
            return f"[无法识别图片内容: {image_path}]"
    
    def _parse_document_file(self, file_path: str) -> Dict[str, Any]:
        """解析文档文件"""
        try:
            file = Path(file_path)
            if not file.exists():
                return {"error": f"文件不存在: {file_path}"}
            
            file_ext = file.suffix.lower()
            
            if file_ext == ".md":
                content = self._read_markdown_file(str(file))
            elif file_ext == ".txt":
                content = self._read_text_file(str(file))
            elif file_ext == ".json":
                content = self._read_json_file(str(file))
            elif file_ext == ".docx":
                content = self._read_docx_file(str(file))
            else:
                return {"error": f"不支持的文件格式: {file_ext}"}
            
            return {
                "source": "document_file",
                "file_path": file_path,
                "file_type": file_ext,
                "extracted_text": content,
                "parsing_method": "file_reading",
                "success": True
            }
            
        except Exception as e:
            return {
                "error": f"处理文档文件时出错: {str(e)}",
                "suggestion": "请检查文件格式和权限"
            }
    
    def _parse_direct_text(self, text: str) -> Dict[str, Any]:
        """解析直接输入的文本"""
        if not text.strip():
            return {"error": "输入文本为空"}
        
        return {
            "source": "direct_text",
            "extracted_text": text.strip(),
            "parsing_method": "direct_input",
            "success": True
        }
    
    def _read_markdown_file(self, file_path: str) -> str:
        """读取Markdown文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _read_text_file(self, file_path: str) -> str:
        """读取文本文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _read_json_file(self, file_path: str) -> str:
        """读取JSON文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return json.dumps(data, indent=2, ensure_ascii=False)
    
    def _read_docx_file(self, file_path: str) -> str:
        """读取Word文档"""
        try:
            from docx import Document
            doc = Document(file_path)
            content = []
            for paragraph in doc.paragraphs:
                content.append(paragraph.text)
            return '\n'.join(content)
        except ImportError:
            return "[需要安装python-docx库来读取Word文档]"
        except Exception as e:
            return f"[读取Word文档失败: {e}]"
    
    def get_supported_formats(self) -> Dict[str, List[str]]:
        """获取支持的格式"""
        return self.supported_formats
    
    def validate_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """验证输入数据"""
        required_fields = ["type", "content"]
        
        for field in required_fields:
            if field not in input_data:
                return {
                    "valid": False,
                    "error": f"缺少必需字段: {field}"
                }
        
        input_type = input_data["type"]
        valid_types = ["codesign_url", "screenshot_folder", "document_file", "direct_text"]
        
        if input_type not in valid_types:
            return {
                "valid": False,
                "error": f"不支持的输入类型: {input_type}，支持的类型: {valid_types}"
            }
        
        return {"valid": True}

# MCP Server 主函数
def main():
    """MCP Server 主入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python 需求文档解析MCP工具.py <input_data_json>")
        print("支持的输入格式:")
        print("1. CodeSign链接: {'type': 'codesign_url', 'content': 'https://...'}")
        print("2. 截图文件夹: {'type': 'screenshot_folder', 'content': '/path/to/screenshots'}")
        print("3. 文档文件: {'type': 'document_file', 'content': '/path/to/document.md'}")
        print("4. 直接文本: {'type': 'direct_text', 'content': '需求内容...'}")
        sys.exit(1)
    
    input_data_json = sys.argv[1]
    
    try:
        input_data = json.loads(input_data_json)
    except json.JSONDecodeError:
        print("Invalid input JSON format")
        sys.exit(1)
    
    parser = RequirementsDocumentParser()
    
    # 验证输入
    validation_result = parser.validate_input(input_data)
    if not validation_result["valid"]:
        print(json.dumps(validation_result, indent=2, ensure_ascii=False))
        sys.exit(1)
    
    # 解析需求
    result = parser.parse_requirements_input(input_data)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
