#!/usr/bin/env python3
"""
项目架构识别 MCP Server
智能识别项目的具体架构模式，然后基于识别结果进行代码生成
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
import ast

class ProjectArchitectureAnalyzer:
    """项目架构分析器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.architecture_profile = {}
        
    def analyze_full_architecture(self) -> Dict[str, Any]:
        """完整架构分析"""
        profile = {
            "project_info": self._detect_project_type(),
            "architecture_patterns": self._detect_architecture_patterns(),
            "layer_structure": self._analyze_layer_structure(),
            "framework_stack": self._detect_framework_stack(),
            "naming_conventions": self._extract_naming_conventions(),
            "code_patterns": self._extract_code_patterns(),
            "database_patterns": self._analyze_database_patterns(),
            "api_patterns": self._analyze_api_patterns(),
            "test_patterns": self._analyze_test_patterns(),
            "build_patterns": self._analyze_build_patterns(),
            "recommendations": self._generate_recommendations()
        }
        
        self.architecture_profile = profile
        return profile
    
    def _detect_project_type(self) -> Dict[str, Any]:
        """检测项目类型和技术栈"""
        project_info = {
            "language": "unknown",
            "project_type": "unknown", 
            "framework": "unknown",
            "build_tool": "unknown",
            "version": "unknown"
        }
        
        # Java项目检测
        if (self.project_root / "pom.xml").exists():
            project_info.update(self._analyze_maven_project())
        elif (self.project_root / "build.gradle").exists():
            project_info.update(self._analyze_gradle_project())
        elif (self.project_root / "build.gradle.kts").exists():
            project_info.update(self._analyze_gradle_kotlin_project())
            
        # Node.js项目检测
        elif (self.project_root / "package.json").exists():
            project_info.update(self._analyze_nodejs_project())
            
        # Python项目检测
        elif (self.project_root / "requirements.txt").exists() or (self.project_root / "pyproject.toml").exists():
            project_info.update(self._analyze_python_project())
            
        # .NET项目检测
        elif list(self.project_root.glob("*.csproj")) or list(self.project_root.glob("*.sln")):
            project_info.update(self._analyze_dotnet_project())
            
        # Go项目检测
        elif (self.project_root / "go.mod").exists():
            project_info.update(self._analyze_go_project())
            
        return project_info
    
    def _detect_architecture_patterns(self) -> List[Dict[str, Any]]:
        """检测架构模式"""
        patterns = []
        
        # 检测分层架构
        layered_pattern = self._detect_layered_architecture()
        if layered_pattern:
            patterns.append(layered_pattern)
            
        # 检测微服务架构
        microservice_pattern = self._detect_microservice_architecture()
        if microservice_pattern:
            patterns.append(microservice_pattern)
            
        # 检测六边形架构
        hexagonal_pattern = self._detect_hexagonal_architecture()
        if hexagonal_pattern:
            patterns.append(hexagonal_pattern)
            
        # 检测DDD架构
        ddd_pattern = self._detect_ddd_architecture()
        if ddd_pattern:
            patterns.append(ddd_pattern)
            
        # 检测CQRS模式
        cqrs_pattern = self._detect_cqrs_pattern()
        if cqrs_pattern:
            patterns.append(cqrs_pattern)
            
        return patterns
    
    def _detect_layered_architecture(self) -> Optional[Dict[str, Any]]:
        """检测分层架构"""
        # 查找常见的分层目录结构
        layer_indicators = {
            "controller": ["controller", "web", "api", "rest"],
            "service": ["service", "business", "logic", "application"],
            "repository": ["repository", "dao", "data", "persistence"],
            "entity": ["entity", "model", "domain", "pojo"],
            "dto": ["dto", "vo", "request", "response"]
        }
        
        found_layers = {}
        confidence = 0
        
        for layer_type, indicators in layer_indicators.items():
            for indicator in indicators:
                # 查找包含指示词的目录
                matching_dirs = list(self.project_root.rglob(f"*{indicator}*"))
                if matching_dirs:
                    found_layers[layer_type] = {
                        "directories": [str(d.relative_to(self.project_root)) for d in matching_dirs],
                        "indicator": indicator
                    }
                    confidence += 20
                    break
        
        if confidence >= 60:  # 至少找到3层
            return {
                "pattern": "Layered Architecture",
                "confidence": min(confidence, 100),
                "layers": found_layers,
                "description": "传统分层架构，按技术职责分层"
            }
        return None
    
    def _detect_microservice_architecture(self) -> Optional[Dict[str, Any]]:
        """检测微服务架构"""
        microservice_indicators = []
        confidence = 0
        
        # 检查多个独立的应用模块
        app_dirs = []
        for pattern in ["*-service", "*-api", "*-app", "service-*", "api-*"]:
            app_dirs.extend(list(self.project_root.glob(pattern)))
        
        if len(app_dirs) >= 2:
            microservice_indicators.append("多个独立服务模块")
            confidence += 30
            
        # 检查Docker配置
        if (self.project_root / "docker-compose.yml").exists():
            microservice_indicators.append("Docker Compose配置")
            confidence += 20
            
        # 检查Kubernetes配置
        k8s_files = list(self.project_root.rglob("*.yaml")) + list(self.project_root.rglob("*.yml"))
        k8s_content = any("apiVersion" in self._read_file_safe(f) for f in k8s_files)
        if k8s_content:
            microservice_indicators.append("Kubernetes配置")
            confidence += 25
            
        # 检查服务发现相关配置
        service_discovery_files = ["eureka", "consul", "nacos", "zookeeper"]
        for sd in service_discovery_files:
            if any(sd in str(f).lower() for f in self.project_root.rglob("*")):
                microservice_indicators.append(f"{sd.capitalize()}服务发现")
                confidence += 15
                break
        
        if confidence >= 50:
            return {
                "pattern": "Microservice Architecture",
                "confidence": min(confidence, 100),
                "indicators": microservice_indicators,
                "services": [str(d.name) for d in app_dirs],
                "description": "微服务架构，多个独立部署的服务"
            }
        return None
    
    def _detect_hexagonal_architecture(self) -> Optional[Dict[str, Any]]:
        """检测六边形架构（端口适配器模式）"""
        hex_indicators = []
        confidence = 0
        
        # 查找端口和适配器相关目录
        port_adapter_dirs = []
        for pattern in ["*port*", "*adapter*", "*infrastructure*", "*application*", "*domain*"]:
            port_adapter_dirs.extend(list(self.project_root.rglob(pattern)))
        
        if len(port_adapter_dirs) >= 3:
            hex_indicators.append("端口适配器目录结构")
            confidence += 40
            
        # 检查接口定义
        interface_files = []
        for java_file in self.project_root.rglob("*.java"):
            content = self._read_file_safe(java_file)
            if "interface" in content and ("Port" in str(java_file) or "Repository" in str(java_file)):
                interface_files.append(java_file)
        
        if len(interface_files) >= 2:
            hex_indicators.append("端口接口定义")
            confidence += 30
            
        if confidence >= 50:
            return {
                "pattern": "Hexagonal Architecture",
                "confidence": min(confidence, 100),
                "indicators": hex_indicators,
                "description": "六边形架构，业务逻辑与外部依赖解耦"
            }
        return None
    
    def _detect_ddd_architecture(self) -> Optional[Dict[str, Any]]:
        """检测领域驱动设计架构"""
        ddd_indicators = []
        confidence = 0
        
        # 查找DDD相关目录结构
        ddd_dirs = []
        for pattern in ["*domain*", "*aggregate*", "*entity*", "*valueobject*", "*repository*", "*service*"]:
            ddd_dirs.extend(list(self.project_root.rglob(pattern)))
        
        # 检查聚合根
        aggregate_files = []
        for java_file in self.project_root.rglob("*.java"):
            content = self._read_file_safe(java_file)
            if any(keyword in content.lower() for keyword in ["aggregateroot", "@aggregate", "aggregate"]):
                aggregate_files.append(java_file)
        
        if aggregate_files:
            ddd_indicators.append("聚合根定义")
            confidence += 35
            
        # 检查值对象
        value_object_files = []
        for java_file in self.project_root.rglob("*.java"):
            if "valueobject" in str(java_file).lower() or "vo" in str(java_file).lower():
                value_object_files.append(java_file)
        
        if value_object_files:
            ddd_indicators.append("值对象定义")
            confidence += 25
            
        # 检查领域服务
        domain_service_files = []
        for java_file in self.project_root.rglob("*.java"):
            if "domainservice" in str(java_file).lower():
                domain_service_files.append(java_file)
        
        if domain_service_files:
            ddd_indicators.append("领域服务")
            confidence += 20
            
        if confidence >= 50:
            return {
                "pattern": "Domain Driven Design",
                "confidence": min(confidence, 100),
                "indicators": ddd_indicators,
                "description": "领域驱动设计，以业务领域为核心"
            }
        return None
    
    def _analyze_layer_structure(self) -> Dict[str, Any]:
        """分析具体的分层结构"""
        structure = {
            "package_structure": self._analyze_package_structure(),
            "directory_hierarchy": self._analyze_directory_hierarchy(),
            "module_dependencies": self._analyze_module_dependencies()
        }
        return structure
    
    def _analyze_package_structure(self) -> Dict[str, List[str]]:
        """分析包结构"""
        packages = {}
        
        # Java包结构分析
        for java_file in self.project_root.rglob("*.java"):
            content = self._read_file_safe(java_file)
            package_match = re.search(r'package\s+([\w.]+);', content)
            if package_match:
                package_name = package_match.group(1)
                parts = package_name.split('.')
                
                # 按层次归类
                for i, part in enumerate(parts):
                    layer_key = f"level_{i}_{part}"
                    if layer_key not in packages:
                        packages[layer_key] = []
                    packages[layer_key].append(str(java_file.relative_to(self.project_root)))
        
        return packages
    
    def _extract_naming_conventions(self) -> Dict[str, Any]:
        """提取命名约定"""
        conventions = {
            "class_naming": self._analyze_class_naming(),
            "method_naming": self._analyze_method_naming(),
            "variable_naming": self._analyze_variable_naming(),
            "package_naming": self._analyze_package_naming(),
            "file_naming": self._analyze_file_naming()
        }
        return conventions
    
    def _analyze_class_naming(self) -> Dict[str, Any]:
        """分析类命名模式"""
        class_names = []
        
        for java_file in self.project_root.rglob("*.java"):
            content = self._read_file_safe(java_file)
            class_matches = re.findall(r'public\s+class\s+([A-Za-z_][A-Za-z0-9_]*)', content)
            class_names.extend(class_matches)
        
        # 分析命名模式
        patterns = {
            "pascal_case": sum(1 for name in class_names if re.match(r'^[A-Z][a-zA-Z0-9]*$', name)),
            "with_suffix": {},
            "with_prefix": {}
        }
        
        # 分析后缀模式
        suffixes = ["Controller", "Service", "Repository", "Entity", "DTO", "Request", "Response"]
        for suffix in suffixes:
            count = sum(1 for name in class_names if name.endswith(suffix))
            if count > 0:
                patterns["with_suffix"][suffix] = count
        
        return {
            "total_classes": len(class_names),
            "patterns": patterns,
            "examples": class_names[:10]
        }
    
    def _extract_code_patterns(self) -> List[Dict[str, Any]]:
        """提取代码模式"""
        patterns = []
        
        # 检测注解使用模式
        annotation_pattern = self._detect_annotation_patterns()
        if annotation_pattern:
            patterns.append(annotation_pattern)
            
        # 检测异常处理模式
        exception_pattern = self._detect_exception_patterns()
        if exception_pattern:
            patterns.append(exception_pattern)
            
        # 检测日志记录模式
        logging_pattern = self._detect_logging_patterns()
        if logging_pattern:
            patterns.append(logging_pattern)
            
        return patterns
    
    def _detect_annotation_patterns(self) -> Optional[Dict[str, Any]]:
        """检测注解使用模式"""
        annotations = {}
        
        for java_file in self.project_root.rglob("*.java"):
            content = self._read_file_safe(java_file)
            # 查找注解
            annotation_matches = re.findall(r'@([A-Za-z][A-Za-z0-9]*)', content)
            for annotation in annotation_matches:
                annotations[annotation] = annotations.get(annotation, 0) + 1
        
        if annotations:
            return {
                "pattern": "Annotation Usage",
                "annotations": annotations,
                "most_used": max(annotations.items(), key=lambda x: x[1]) if annotations else None
            }
        return None
    
    def _generate_recommendations(self) -> List[Dict[str, str]]:
        """生成架构建议"""
        recommendations = []
        
        # 基于检测到的架构模式给出建议
        if self.architecture_profile.get("architecture_patterns"):
            for pattern in self.architecture_profile["architecture_patterns"]:
                if pattern["pattern"] == "Layered Architecture":
                    recommendations.append({
                        "type": "architecture",
                        "title": "分层架构优化建议",
                        "description": "建议保持严格的分层依赖关系，避免跨层调用"
                    })
                elif pattern["pattern"] == "Microservice Architecture":
                    recommendations.append({
                        "type": "architecture", 
                        "title": "微服务架构建议",
                        "description": "建议实现服务间的熔断、限流和监控机制"
                    })
        
        return recommendations
    
    # 辅助方法
    def _read_file_safe(self, file_path: Path) -> str:
        """安全读取文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return ""
    
    def _analyze_maven_project(self) -> Dict[str, str]:
        """分析Maven项目"""
        pom_content = self._read_file_safe(self.project_root / "pom.xml")
        
        # 提取Spring Boot版本
        spring_boot_match = re.search(r'<spring-boot\.version>([^<]+)</spring-boot\.version>', pom_content)
        if not spring_boot_match:
            spring_boot_match = re.search(r'<version>([^<]+)</version>.*spring-boot', pom_content, re.DOTALL)
        
        framework = "unknown"
        if "spring-boot" in pom_content:
            framework = "Spring Boot"
        elif "spring" in pom_content:
            framework = "Spring"
        
        return {
            "language": "java",
            "project_type": "maven",
            "build_tool": "maven",
            "framework": framework,
            "version": spring_boot_match.group(1) if spring_boot_match else "unknown"
        }
    
    def _analyze_nodejs_project(self) -> Dict[str, str]:
        """分析Node.js项目"""
        try:
            with open(self.project_root / "package.json", 'r') as f:
                package_data = json.load(f)
            
            framework = "unknown"
            dependencies = package_data.get("dependencies", {})
            
            if "express" in dependencies:
                framework = "Express"
            elif "koa" in dependencies:
                framework = "Koa"
            elif "fastify" in dependencies:
                framework = "Fastify"
            elif "next" in dependencies:
                framework = "Next.js"
            elif "nuxt" in dependencies:
                framework = "Nuxt.js"
            
            return {
                "language": "javascript",
                "project_type": "nodejs",
                "build_tool": "npm",
                "framework": framework,
                "version": package_data.get("version", "unknown")
            }
        except:
            return {"language": "javascript", "project_type": "nodejs"}

# MCP Server 主函数
def main():
    """MCP Server 主入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python project-architecture-analyzer.py <project_root>")
        sys.exit(1)
    
    project_root = sys.argv[1]
    analyzer = ProjectArchitectureAnalyzer(project_root)
    architecture_profile = analyzer.analyze_full_architecture()
    
    print(json.dumps(architecture_profile, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
