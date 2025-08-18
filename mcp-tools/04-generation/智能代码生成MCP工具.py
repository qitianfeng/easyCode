#!/usr/bin/env python3
"""
智能代码生成 MCP Server
基于项目架构识别结果，生成符合项目特定架构的代码
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

class IntelligentCodeGenerator:
    """智能代码生成器"""
    
    def __init__(self, project_root: str, architecture_profile: Dict[str, Any]):
        self.project_root = Path(project_root)
        self.architecture_profile = architecture_profile
        self.templates = self._load_architecture_templates()
    
    def generate_module_by_architecture(self, module_name: str, fields: List[Dict]) -> Dict[str, str]:
        """根据架构模式生成模块代码"""
        architecture_patterns = self.architecture_profile.get("architecture_patterns", [])
        
        if not architecture_patterns:
            return self._generate_default_module(module_name, fields)
        
        # 根据主要架构模式选择生成策略
        primary_pattern = architecture_patterns[0]["pattern"]
        
        if primary_pattern == "Layered Architecture":
            return self._generate_layered_module(module_name, fields)
        elif primary_pattern == "Microservice Architecture":
            return self._generate_microservice_module(module_name, fields)
        elif primary_pattern == "Hexagonal Architecture":
            return self._generate_hexagonal_module(module_name, fields)
        elif primary_pattern == "Domain Driven Design":
            return self._generate_ddd_module(module_name, fields)
        else:
            return self._generate_default_module(module_name, fields)
    
    def _generate_layered_module(self, module_name: str, fields: List[Dict]) -> Dict[str, str]:
        """生成分层架构模块"""
        generated_files = {}
        
        # 获取项目的分层结构
        layer_structure = self.architecture_profile.get("layer_structure", {})
        naming_conventions = self.architecture_profile.get("naming_conventions", {})
        
        # 根据实际的包结构生成代码
        base_package = self._extract_base_package()
        
        # 生成Entity（根据实际的entity层位置）
        entity_package = self._find_layer_package("entity", base_package)
        generated_files[f"{module_name}.java"] = self._generate_layered_entity(
            module_name, fields, entity_package
        )
        
        # 生成Repository（根据实际的repository层位置）
        repo_package = self._find_layer_package("repository", base_package)
        generated_files[f"{module_name}Repository.java"] = self._generate_layered_repository(
            module_name, repo_package, entity_package
        )
        
        # 生成Service（根据实际的service层位置）
        service_package = self._find_layer_package("service", base_package)
        generated_files[f"{module_name}Service.java"] = self._generate_layered_service(
            module_name, service_package, repo_package, entity_package
        )
        
        # 生成Controller（根据实际的controller层位置）
        controller_package = self._find_layer_package("controller", base_package)
        generated_files[f"{module_name}Controller.java"] = self._generate_layered_controller(
            module_name, controller_package, service_package, entity_package
        )
        
        return generated_files
    
    def _generate_microservice_module(self, module_name: str, fields: List[Dict]) -> Dict[str, str]:
        """生成微服务架构模块"""
        generated_files = {}
        
        # 微服务架构通常每个服务都是独立的
        service_name = f"{module_name.lower()}-service"
        
        # 生成服务的完整结构
        generated_files.update(self._generate_microservice_structure(module_name, fields, service_name))
        
        # 生成Docker配置
        generated_files["Dockerfile"] = self._generate_dockerfile(service_name)
        
        # 生成服务配置
        generated_files["application.yml"] = self._generate_microservice_config(service_name)
        
        # 生成API网关配置（如果需要）
        generated_files["gateway-config.yml"] = self._generate_gateway_config(service_name)
        
        return generated_files
    
    def _generate_hexagonal_module(self, module_name: str, fields: List[Dict]) -> Dict[str, str]:
        """生成六边形架构模块"""
        generated_files = {}
        
        base_package = self._extract_base_package()
        
        # Domain层（核心业务逻辑）
        domain_package = f"{base_package}.domain.{module_name.lower()}"
        generated_files[f"{module_name}.java"] = self._generate_domain_entity(
            module_name, fields, domain_package
        )
        generated_files[f"{module_name}Repository.java"] = self._generate_domain_port(
            module_name, domain_package
        )
        generated_files[f"{module_name}Service.java"] = self._generate_domain_service(
            module_name, domain_package
        )
        
        # Infrastructure层（适配器）
        infra_package = f"{base_package}.infrastructure.{module_name.lower()}"
        generated_files[f"{module_name}RepositoryImpl.java"] = self._generate_repository_adapter(
            module_name, infra_package, domain_package
        )
        generated_files[f"{module_name}JpaRepository.java"] = self._generate_jpa_repository(
            module_name, infra_package
        )
        
        # Application层（应用服务）
        app_package = f"{base_package}.application.{module_name.lower()}"
        generated_files[f"{module_name}ApplicationService.java"] = self._generate_application_service(
            module_name, app_package, domain_package
        )
        
        # Web层（Web适配器）
        web_package = f"{base_package}.web.{module_name.lower()}"
        generated_files[f"{module_name}Controller.java"] = self._generate_web_adapter(
            module_name, web_package, app_package
        )
        
        return generated_files
    
    def _generate_ddd_module(self, module_name: str, fields: List[Dict]) -> Dict[str, str]:
        """生成DDD架构模块"""
        generated_files = {}
        
        base_package = self._extract_base_package()
        domain_package = f"{base_package}.domain.{module_name.lower()}"
        
        # 聚合根
        generated_files[f"{module_name}Aggregate.java"] = self._generate_aggregate_root(
            module_name, fields, domain_package
        )
        
        # 值对象
        for field in fields:
            if field.get("is_value_object", False):
                vo_name = f"{field['name'].capitalize()}VO"
                generated_files[f"{vo_name}.java"] = self._generate_value_object(
                    vo_name, field, domain_package
                )
        
        # 领域服务
        generated_files[f"{module_name}DomainService.java"] = self._generate_domain_service_ddd(
            module_name, domain_package
        )
        
        # 仓储接口
        generated_files[f"{module_name}Repository.java"] = self._generate_ddd_repository(
            module_name, domain_package
        )
        
        # 应用服务
        app_package = f"{base_package}.application.{module_name.lower()}"
        generated_files[f"{module_name}ApplicationService.java"] = self._generate_ddd_application_service(
            module_name, app_package, domain_package
        )
        
        # 基础设施层实现
        infra_package = f"{base_package}.infrastructure.{module_name.lower()}"
        generated_files[f"{module_name}RepositoryImpl.java"] = self._generate_ddd_repository_impl(
            module_name, infra_package, domain_package
        )
        
        return generated_files
    
    def _extract_base_package(self) -> str:
        """提取项目的基础包名"""
        package_structure = self.architecture_profile.get("layer_structure", {}).get("package_structure", {})
        
        # 从包结构中提取最常见的基础包
        base_packages = []
        for key, files in package_structure.items():
            if "level_" in key and files:
                # 提取包名的前几层
                parts = key.split("_")
                if len(parts) >= 3:
                    base_packages.append(".".join(parts[2:4]))  # 取前两层
        
        if base_packages:
            # 返回最常见的基础包
            from collections import Counter
            return Counter(base_packages).most_common(1)[0][0]
        
        # 默认包名
        return "com.example.project"
    
    def _find_layer_package(self, layer_type: str, base_package: str) -> str:
        """查找特定层的包名"""
        layer_structure = self.architecture_profile.get("layer_structure", {})
        
        # 从架构分析结果中查找对应层的包名
        architecture_patterns = self.architecture_profile.get("architecture_patterns", [])
        for pattern in architecture_patterns:
            if pattern["pattern"] == "Layered Architecture":
                layers = pattern.get("layers", {})
                if layer_type in layers:
                    # 使用检测到的层目录结构
                    directories = layers[layer_type]["directories"]
                    if directories:
                        # 转换目录路径为包名
                        dir_path = directories[0].replace("/", ".").replace("\\", ".")
                        return f"{base_package}.{dir_path}"
        
        # 默认包名
        return f"{base_package}.{layer_type}"
    
    def _generate_layered_entity(self, entity_name: str, fields: List[Dict], package_name: str) -> str:
        """生成分层架构的实体类"""
        # 获取项目的注解使用模式
        code_patterns = self.architecture_profile.get("code_patterns", [])
        annotation_pattern = next((p for p in code_patterns if p.get("pattern") == "Annotation Usage"), None)
        
        # 根据项目实际使用的注解生成代码
        annotations = []
        if annotation_pattern:
            common_annotations = annotation_pattern.get("annotations", {})
            if "Entity" in common_annotations:
                annotations.append("@Entity")
            if "Table" in common_annotations:
                annotations.append(f'@Table(name = "{self._to_snake_case(entity_name)}s")')
        
        template = f'''package {package_name};

import javax.persistence.*;
import javax.validation.constraints.*;
import java.time.LocalDateTime;
import java.util.Objects;

/**
 * {entity_name}实体类
 * 根据项目架构自动生成
 */
{chr(10).join(annotations)}
public class {entity_name} {{
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
{self._generate_entity_fields(fields)}
    
    // 根据项目模式生成的标准字段
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @Column(name = "updated_at", nullable = false)
    private LocalDateTime updatedAt;
    
    @PrePersist
    protected void onCreate() {{
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }}
    
    @PreUpdate
    protected void onUpdate() {{
        updatedAt = LocalDateTime.now();
    }}
    
    // 构造函数
    public {entity_name}() {{}}
    
{self._generate_getters_setters(entity_name, fields)}
    
    @Override
    public boolean equals(Object o) {{
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        {entity_name} {entity_name.lower()} = ({entity_name}) o;
        return Objects.equals(id, {entity_name.lower()}.id);
    }}
    
    @Override
    public int hashCode() {{
        return Objects.hash(id);
    }}
}}'''
        return template
    
    def _generate_aggregate_root(self, entity_name: str, fields: List[Dict], package_name: str) -> str:
        """生成DDD聚合根"""
        template = f'''package {package_name};

import {package_name}.event.*;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

/**
 * {entity_name}聚合根
 * DDD架构模式
 */
public class {entity_name}Aggregate {{
    
    private {entity_name}Id id;
{self._generate_ddd_fields(fields)}
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    private List<DomainEvent> domainEvents = new ArrayList<>();
    
    // 构造函数
    public {entity_name}Aggregate({entity_name}Id id) {{
        this.id = id;
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }}
    
    // 业务方法
    public void update{entity_name}({self._generate_method_params(fields)}) {{
{self._generate_update_logic(fields)}
        this.updatedAt = LocalDateTime.now();
        
        // 发布领域事件
        this.domainEvents.add(new {entity_name}UpdatedEvent(this.id));
    }}
    
    // 获取领域事件
    public List<DomainEvent> getDomainEvents() {{
        return new ArrayList<>(domainEvents);
    }}
    
    // 清除领域事件
    public void clearDomainEvents() {{
        domainEvents.clear();
    }}
    
{self._generate_ddd_getters(entity_name, fields)}
}}'''
        return template
    
    # 辅助方法
    def _load_architecture_templates(self) -> Dict[str, str]:
        """加载架构特定的模板"""
        return {}
    
    def _to_snake_case(self, name: str) -> str:
        """转换为snake_case"""
        import re
        return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name).lower()
    
    def _generate_entity_fields(self, fields: List[Dict]) -> str:
        """生成实体字段"""
        field_code = ""
        for field in fields:
            field_code += f'''    
    @Column(name = "{self._to_snake_case(field['name'])}")
    private {field['type']} {field['name']};
'''
        return field_code
    
    def _generate_getters_setters(self, entity_name: str, fields: List[Dict]) -> str:
        """生成getter和setter方法"""
        code = ""
        
        # 标准字段
        standard_fields = [
            {"name": "id", "type": "Long"},
            {"name": "createdAt", "type": "LocalDateTime"},
            {"name": "updatedAt", "type": "LocalDateTime"}
        ]
        
        all_fields = fields + standard_fields
        
        for field in all_fields:
            field_name = field['name']
            field_type = field['type']
            capitalized_name = field_name.capitalize()
            
            code += f'''    
    public {field_type} get{capitalized_name}() {{
        return {field_name};
    }}
    
    public void set{capitalized_name}({field_type} {field_name}) {{
        this.{field_name} = {field_name};
    }}
'''
        
        return code
    
    def _generate_ddd_fields(self, fields: List[Dict]) -> str:
        """生成DDD字段"""
        field_code = ""
        for field in fields:
            if field.get("is_value_object", False):
                field_code += f"    private {field['name'].capitalize()}VO {field['name']};\n"
            else:
                field_code += f"    private {field['type']} {field['name']};\n"
        return field_code

# MCP Server 主函数
def main():
    """MCP Server 主入口"""
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python intelligent-code-generator.py <project_root> <architecture_profile_json> <module_name> <fields_json>")
        sys.exit(1)
    
    project_root = sys.argv[1]
    architecture_profile_json = sys.argv[2]
    module_name = sys.argv[3]
    fields_json = sys.argv[4]
    
    try:
        architecture_profile = json.loads(architecture_profile_json)
        fields = json.loads(fields_json)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON format: {e}")
        sys.exit(1)
    
    generator = IntelligentCodeGenerator(project_root, architecture_profile)
    generated_files = generator.generate_module_by_architecture(module_name, fields)
    
    print(json.dumps(generated_files, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
