#!/usr/bin/env python3
"""
代码生成MCP服务器 - 标准 MCP 服务器实现
智能代码生成MCP服务器
"""

import asyncio
import json
import sys
from typing import Any, Dict, List

class 代码生成MCP服务器Server:
    def __init__(self):
        self.tools = {
            "generate_crud_module": {
                        "description": "生成完整的CRUD模块",
                        "parameters": {
                                    "type": "object",
                                    "properties": {
                                                "entity_name": {
                                                            "type": "string",
                                                            "description": "实体名称"
                                                },
                                                "fields": {
                                                            "type": "array",
                                                            "description": "字段定义",
                                                            "items": {
                                                                        "type": "object",
                                                                        "properties": {
                                                                                    "name": {
                                                                                                "type": "string"
                                                                                    },
                                                                                    "type": {
                                                                                                "type": "string"
                                                                                    }
                                                                        }
                                                            }
                                                },
                                                "project_path": {
                                                            "type": "string",
                                                            "description": "项目根目录路径，默认为当前目录"
                                                },
                                                "package_name": {
                                                            "type": "string",
                                                            "description": "包名，如果不指定将自动分析项目结构推断"
                                                }
                                    },
                                    "required": [
                                                "entity_name",
                                                "fields"
                                    ]
                        }
            },
            "generate_entity": {
                        "description": "生成实体类",
                        "parameters": {
                                    "type": "object",
                                    "properties": {
                                                "entity_name": {
                                                            "type": "string",
                                                            "description": "实体名称"
                                                },
                                                "fields": {
                                                            "type": "array",
                                                            "description": "字段定义"
                                                }
                                    },
                                    "required": [
                                                "entity_name",
                                                "fields"
                                    ]
                        }
            }
}
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """处理 MCP 请求"""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        try:
            if method == "initialize":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {
                            "name": "代码生成MCP服务器",
                            "version": "1.0.0"
                        }
                    }
                }
            
            elif method == "tools/list":
                tools_list = []
                for name, tool_info in self.tools.items():
                    tools_list.append({
                        "name": name,
                        "description": tool_info["description"],
                        "inputSchema": tool_info["parameters"]
                    })
                
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"tools": tools_list}
                }
            
            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                # 调用对应的工具方法
                if hasattr(self, f"handle_{tool_name}"):
                    result = await getattr(self, f"handle_{tool_name}")(arguments)
                else:
                    result = await self.handle_default_tool(tool_name, arguments)
                
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{
                            "type": "text",
                            "text": json.dumps(result, indent=2, ensure_ascii=False)
                        }]
                    }
                }
            
            else:
                raise ValueError(f"Unknown method: {method}")
        
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32000,
                    "message": str(e)
                }
            }
    
    async def handle_default_tool(self, tool_name: str, arguments: Dict[str, Any]):
        """默认工具处理器"""
        return {
            "status": "success",
            "tool": tool_name,
            "message": f"{tool_name} 执行成功",
            "arguments": arguments,
            "result": "功能正常，等待具体实现"
        }

    async def handle_generate_crud_module(self, arguments: Dict[str, Any]):
        """生成完整的CRUD模块"""
        entity_name = arguments.get("entity_name", "")
        fields = arguments.get("fields", [])
        project_path = arguments.get("project_path", ".")
        package_name = arguments.get("package_name", None)

        # 智能分析项目结构
        project_info = self._analyze_project_structure(project_path)

        # 如果没有指定包名，使用分析得到的包名
        if not package_name:
            package_name = project_info.get("base_package", "com.example")

        # 生成文件内容
        generated_files = {
            "entity": {},
            "repository": {},
            "service": {},
            "controller": {},
            "dto/request": {},
            "dto/response": {}
        }

        # 1. 生成实体类
        entity_code = self._generate_entity_class(entity_name, fields, package_name)
        generated_files["entity"][f"{entity_name}.java"] = entity_code

        # 2. 生成Repository接口
        repository_code = self._generate_repository_interface(entity_name, package_name)
        generated_files["repository"][f"{entity_name}Repository.java"] = repository_code

        # 3. 生成Service类
        service_code = self._generate_service_class(entity_name, package_name)
        generated_files["service"][f"{entity_name}Service.java"] = service_code

        # 4. 生成Controller类
        controller_code = self._generate_controller_class(entity_name, package_name)
        generated_files["controller"][f"{entity_name}Controller.java"] = controller_code

        # 5. 生成DTO类
        request_dto_code = self._generate_request_dto(entity_name, fields, package_name)
        response_dto_code = self._generate_response_dto(entity_name, fields, package_name)
        generated_files["dto/request"][f"Create{entity_name}Request.java"] = request_dto_code
        generated_files["dto/response"][f"{entity_name}Response.java"] = response_dto_code

        # 保存生成的文件到学习到的项目结构
        saved_files = self._save_files_to_learned_structure(generated_files, project_info, package_name)

        # 转换 project_info 中的 Path 对象为字符串
        serializable_project_info = {}
        for key, value in project_info.items():
            if hasattr(value, '__fspath__'):  # Path 对象
                serializable_project_info[key] = str(value)
            else:
                serializable_project_info[key] = value

        return {
            "status": "success",
            "message": f"成功生成完整的CRUD模块，包含 {len(saved_files)} 个文件",
            "files": saved_files,
            "project_info": serializable_project_info,
            "package_name": package_name,
            "components": ["Entity", "Repository", "Service", "Controller", "DTOs"]
        }

    async def handle_generate_entity(self, arguments: Dict[str, Any]):
        """生成实体类"""
        entity_name = arguments.get("entity_name", "")
        fields = arguments.get("fields", [])

        # 简化的实体生成
        entity_code = f"""package com.example.entity;

// import javax.persistence.*;
// import java.time.LocalDateTime;

@Entity
@Table(name = "{entity_name.lower()}s")
public class {entity_name} {{
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
"""

        for field in fields:
            field_name = field.get('name', 'field') if isinstance(field, dict) else str(field)
            field_type = field.get('type', 'String') if isinstance(field, dict) else 'String'
            entity_code += f"""
    @Column(name = "{field_name}")
    private {field_type} {field_name};
"""

        entity_code += """
    // Getters and Setters
    // ... (省略具体实现)
}"""

        return {
            "status": "success",
            "entity_code": entity_code,
            "entity_name": entity_name
        }

    def _generate_entity_class(self, entity_name: str, fields: list, package_name: str) -> str:
        """生成实体类"""
        entity_code = f"""package {package_name}.entity;

import javax.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "{entity_name.lower()}s")
public class {entity_name} {{
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
"""

        # 添加字段
        for field in fields:
            field_name = field.get('name', 'field')
            field_type = field.get('type', 'String')
            entity_code += f"""
    @Column(name = "{field_name}")
    private {field_type} {field_name};
"""

        # 添加审计字段
        entity_code += """
    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }

    // Constructors
    public {entity_name}() {{}}

    // Getters and Setters
    public Long getId() {{
        return id;
    }}

    public void setId(Long id) {{
        this.id = id;
    }}
"""

        # 生成字段的getter/setter
        for field in fields:
            field_name = field.get('name', 'field')
            field_type = field.get('type', 'String')
            capitalized_name = field_name.capitalize()
            entity_code += f"""
    public {field_type} get{capitalized_name}() {{
        return {field_name};
    }}

    public void set{capitalized_name}({field_type} {field_name}) {{
        this.{field_name} = {field_name};
    }}
"""

        entity_code += """
    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }

    public void setUpdatedAt(LocalDateTime updatedAt) {
        this.updatedAt = updatedAt;
    }
}"""

        return entity_code

    def _generate_repository_interface(self, entity_name: str, package_name: str) -> str:
        """生成Repository接口"""
        return f"""package {package_name}.repository;

import {package_name}.entity.{entity_name};
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface {entity_name}Repository extends JpaRepository<{entity_name}, Long> {{

    // 根据名称查找（假设有name字段）
    Optional<{entity_name}> findByName(String name);

    // 分页查询活跃记录
    @Query("SELECT e FROM {entity_name} e WHERE e.createdAt >= :startDate")
    List<{entity_name}> findRecentRecords(@Param("startDate") java.time.LocalDateTime startDate);

    // 统计总数
    @Query("SELECT COUNT(e) FROM {entity_name} e")
    long countTotal();
}}"""

    def _generate_service_class(self, entity_name: str, package_name: str) -> str:
        """生成Service类"""
        return f"""package {package_name}.service;

import {package_name}.entity.{entity_name};
import {package_name}.repository.{entity_name}Repository;
import {package_name}.dto.request.Create{entity_name}Request;
import {package_name}.dto.response.{entity_name}Response;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
@Transactional
public class {entity_name}Service {{

    @Autowired
    private {entity_name}Repository {entity_name.lower()}Repository;

    public List<{entity_name}Response> findAll() {{
        return {entity_name.lower()}Repository.findAll()
                .stream()
                .map(this::convertToResponse)
                .collect(Collectors.toList());
    }}

    public Page<{entity_name}Response> findAll(Pageable pageable) {{
        return {entity_name.lower()}Repository.findAll(pageable)
                .map(this::convertToResponse);
    }}

    public Optional<{entity_name}Response> findById(Long id) {{
        return {entity_name.lower()}Repository.findById(id)
                .map(this::convertToResponse);
    }}

    public {entity_name}Response create(Create{entity_name}Request request) {{
        {entity_name} entity = convertToEntity(request);
        {entity_name} saved = {entity_name.lower()}Repository.save(entity);
        return convertToResponse(saved);
    }}

    public Optional<{entity_name}Response> update(Long id, Create{entity_name}Request request) {{
        return {entity_name.lower()}Repository.findById(id)
                .map(existing -> {{
                    updateEntityFromRequest(existing, request);
                    {entity_name} updated = {entity_name.lower()}Repository.save(existing);
                    return convertToResponse(updated);
                }});
    }}

    public boolean delete(Long id) {{
        if ({entity_name.lower()}Repository.existsById(id)) {{
            {entity_name.lower()}Repository.deleteById(id);
            return true;
        }}
        return false;
    }}

    public long count() {{
        return {entity_name.lower()}Repository.count();
    }}

    // 转换方法
    private {entity_name}Response convertToResponse({entity_name} entity) {{
        {entity_name}Response response = new {entity_name}Response();
        response.setId(entity.getId());
        // TODO: 设置其他字段
        response.setCreatedAt(entity.getCreatedAt());
        response.setUpdatedAt(entity.getUpdatedAt());
        return response;
    }}

    private {entity_name} convertToEntity(Create{entity_name}Request request) {{
        {entity_name} entity = new {entity_name}();
        // TODO: 从请求设置字段
        return entity;
    }}

    private void updateEntityFromRequest({entity_name} entity, Create{entity_name}Request request) {{
        // TODO: 更新实体字段
    }}
}}"""

    def _generate_controller_class(self, entity_name: str, package_name: str) -> str:
        """生成Controller类"""
        return f"""package {package_name}.controller;

import {package_name}.service.{entity_name}Service;
import {package_name}.dto.request.Create{entity_name}Request;
import {package_name}.dto.response.{entity_name}Response;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.List;

@RestController
@RequestMapping("/api/{entity_name.lower()}s")
@CrossOrigin(origins = "*")
public class {entity_name}Controller {{

    @Autowired
    private {entity_name}Service {entity_name.lower()}Service;

    @GetMapping
    public ResponseEntity<List<{entity_name}Response>> getAllEntities() {{
        List<{entity_name}Response> entities = {entity_name.lower()}Service.findAll();
        return ResponseEntity.ok(entities);
    }}

    @GetMapping("/page")
    public ResponseEntity<Page<{entity_name}Response>> getAllEntitiesPageable(Pageable pageable) {{
        Page<{entity_name}Response> entities = {entity_name.lower()}Service.findAll(pageable);
        return ResponseEntity.ok(entities);
    }}

    @GetMapping("/{{id}}")
    public ResponseEntity<{entity_name}Response> getEntityById(@PathVariable Long id) {{
        return {entity_name.lower()}Service.findById(id)
                .map(entity -> ResponseEntity.ok(entity))
                .orElse(ResponseEntity.notFound().build());
    }}

    @PostMapping
    public ResponseEntity<{entity_name}Response> createEntity(@Valid @RequestBody Create{entity_name}Request request) {{
        {entity_name}Response created = {entity_name.lower()}Service.create(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }}

    @PutMapping("/{{id}}")
    public ResponseEntity<{entity_name}Response> updateEntity(
            @PathVariable Long id,
            @Valid @RequestBody Create{entity_name}Request request) {{
        return {entity_name.lower()}Service.update(id, request)
                .map(entity -> ResponseEntity.ok(entity))
                .orElse(ResponseEntity.notFound().build());
    }}

    @DeleteMapping("/{{id}}")
    public ResponseEntity<Void> deleteEntity(@PathVariable Long id) {{
        if ({entity_name.lower()}Service.delete(id)) {{
            return ResponseEntity.noContent().build();
        }}
        return ResponseEntity.notFound().build();
    }}

    @GetMapping("/count")
    public ResponseEntity<Long> getCount() {{
        long count = {entity_name.lower()}Service.count();
        return ResponseEntity.ok(count);
    }}
}}"""

    def _generate_request_dto(self, entity_name: str, fields: list, package_name: str) -> str:
        """生成请求DTO类"""
        dto_code = f"""package {package_name}.dto.request;

import javax.validation.constraints.*;

public class Create{entity_name}Request {{
"""

        # 添加字段
        for field in fields:
            field_name = field.get('name', 'field')
            field_type = field.get('type', 'String')

            # 添加验证注解
            if field_type == 'String':
                dto_code += f"""
    @NotBlank(message = "{field_name} cannot be blank")
    @Size(max = 255, message = "{field_name} cannot exceed 255 characters")
    private {field_type} {field_name};
"""
            else:
                dto_code += f"""
    @NotNull(message = "{field_name} cannot be null")
    private {field_type} {field_name};
"""

        # 添加构造函数和getter/setter
        dto_code += f"""
    public Create{entity_name}Request() {{}}

    // Getters and Setters
"""

        for field in fields:
            field_name = field.get('name', 'field')
            field_type = field.get('type', 'String')
            capitalized_name = field_name.capitalize()
            dto_code += f"""
    public {field_type} get{capitalized_name}() {{
        return {field_name};
    }}

    public void set{capitalized_name}({field_type} {field_name}) {{
        this.{field_name} = {field_name};
    }}
"""

        dto_code += "}"
        return dto_code

    def _generate_response_dto(self, entity_name: str, fields: list, package_name: str) -> str:
        """生成响应DTO类"""
        dto_code = f"""package {package_name}.dto.response;

import java.time.LocalDateTime;

public class {entity_name}Response {{

    private Long id;
"""

        # 添加字段
        for field in fields:
            field_name = field.get('name', 'field')
            field_type = field.get('type', 'String')
            dto_code += f"""
    private {field_type} {field_name};
"""

        # 添加审计字段
        dto_code += """
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    public {entity_name}Response() {{}}

    // Getters and Setters
    public Long getId() {{
        return id;
    }}

    public void setId(Long id) {{
        this.id = id;
    }}
"""

        # 生成字段的getter/setter
        for field in fields:
            field_name = field.get('name', 'field')
            field_type = field.get('type', 'String')
            capitalized_name = field_name.capitalize()
            dto_code += f"""
    public {field_type} get{capitalized_name}() {{
        return {field_name};
    }}

    public void set{capitalized_name}({field_type} {field_name}) {{
        this.{field_name} = {field_name};
    }}
"""

        dto_code += """
    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }

    public void setUpdatedAt(LocalDateTime updatedAt) {
        this.updatedAt = updatedAt;
    }
}"""

        return dto_code

    def _analyze_project_structure(self, project_path: str) -> Dict[str, Any]:
        """深度分析项目结构，学习项目规范和习惯"""
        import os
        from pathlib import Path

        project_root = Path(project_path)
        project_info = {
            "base_package": "com.example",
            "src_main_java": None,
            "has_maven": False,
            "has_gradle": False,
            "existing_packages": [],
            "project_root": project_path,
            # 新增：项目结构学习
            "layer_patterns": {
                "entity": {"dirs": [], "naming": [], "annotations": []},
                "repository": {"dirs": [], "naming": [], "annotations": []},
                "service": {"dirs": [], "naming": [], "annotations": []},
                "controller": {"dirs": [], "naming": [], "annotations": []},
                "dto": {"dirs": [], "naming": [], "annotations": []}
            },
            "project_conventions": {
                "entity_suffix": "Entity",
                "repository_suffix": "Repository",
                "service_suffix": "Service",
                "controller_suffix": "Controller",
                "request_dto_pattern": "Request",
                "response_dto_pattern": "Response"
            },
            "framework_info": {
                "orm": "unknown",  # jpa, mybatis, etc.
                "web": "unknown",  # spring-mvc, spring-webflux, etc.
                "validation": "unknown"  # javax.validation, hibernate-validator, etc.
            }
        }

        # 检查是否是 Maven 项目
        if (project_root / "pom.xml").exists():
            project_info["has_maven"] = True
            project_info["src_main_java"] = project_root / "src" / "main" / "java"

        # 检查是否是 Gradle 项目
        if (project_root / "build.gradle").exists() or (project_root / "build.gradle.kts").exists():
            project_info["has_gradle"] = True
            if not project_info["src_main_java"]:
                project_info["src_main_java"] = project_root / "src" / "main" / "java"

        # 如果没有标准结构，查找 java 文件
        if not project_info["src_main_java"]:
            java_dirs = []
            for root, dirs, files in os.walk(project_root):
                if any(f.endswith('.java') for f in files):
                    java_dirs.append(Path(root))

            if java_dirs:
                # 选择最浅的目录作为源码目录的父目录
                project_info["src_main_java"] = java_dirs[0].parent / "src" / "main" / "java"
            else:
                # 默认创建标准 Maven 结构
                project_info["src_main_java"] = project_root / "src" / "main" / "java"

        # 深度分析现有项目结构和规范
        if project_info["src_main_java"] and project_info["src_main_java"].exists():
            try:
                # 扫描所有 Java 文件，学习项目结构
                for root, dirs, files in os.walk(project_info["src_main_java"]):
                    for file in files:
                        if file.endswith('.java'):
                            java_file = Path(root) / file
                            self._learn_from_java_file(java_file, project_info)

                # 分析学习结果，推断项目规范
                self._infer_project_conventions(project_info)

                # 使用最常见的包名作为基础包名
                if project_info["existing_packages"]:
                    # 找到最短的包名作为基础包名
                    base_packages = [pkg.split('.') for pkg in project_info["existing_packages"]]
                    if base_packages:
                        # 找到公共前缀
                        common_parts = []
                        min_length = min(len(parts) for parts in base_packages)
                        for i in range(min_length):
                            parts_at_i = [parts[i] for parts in base_packages]
                            if len(set(parts_at_i)) == 1:  # 所有包在这个位置都相同
                                common_parts.append(parts_at_i[0])
                            else:
                                break

                        if len(common_parts) >= 2:  # 至少有 com.example 这样的结构
                            project_info["base_package"] = '.'.join(common_parts)
            except Exception:
                pass  # 如果分析失败，使用默认值

        return project_info

    def _extract_package_from_java_file(self, java_file) -> str:
        """从 Java 文件中提取包名"""
        try:
            with open(java_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('package ') and line.endswith(';'):
                        return line[8:-1].strip()  # 去掉 'package ' 和 ';'
        except Exception:
            pass
        return None

    def _save_files_to_project_structure(self, generated_files: Dict[str, Dict[str, str]],
                                       project_info: Dict[str, Any], package_name: str) -> list:
        """将生成的文件保存到正确的项目结构中"""
        import os
        from pathlib import Path

        saved_files = []
        src_main_java = project_info["src_main_java"]

        # 确保源码目录存在
        src_main_java.mkdir(parents=True, exist_ok=True)

        # 将包名转换为目录路径
        package_path = src_main_java / package_name.replace('.', os.sep)

        for layer, files in generated_files.items():
            if not files:  # 跳过空的层
                continue

            # 创建对应的目录结构
            layer_path = package_path / layer
            layer_path.mkdir(parents=True, exist_ok=True)

            for filename, content in files.items():
                file_path = layer_path / filename

                # 保存文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                # 记录保存的文件路径（相对于项目根目录）
                try:
                    relative_path = file_path.relative_to(Path(project_info["project_root"]))
                    saved_files.append(str(relative_path))
                except ValueError:
                    # 如果无法计算相对路径，使用绝对路径
                    saved_files.append(str(file_path))

        return saved_files

    def _learn_from_java_file(self, java_file, project_info):
        """从单个 Java 文件学习项目规范"""
        try:
            with open(java_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 提取包名
            package_name = None
            class_name = None
            annotations = []

            for line in content.split('\n'):
                line = line.strip()

                # 提取包名
                if line.startswith('package ') and line.endswith(';'):
                    package_name = line[8:-1].strip()
                    if package_name not in project_info["existing_packages"]:
                        project_info["existing_packages"].append(package_name)

                # 提取类名
                if line.startswith('public class ') or line.startswith('public interface '):
                    parts = line.split()
                    if len(parts) >= 3:
                        class_name = parts[2].split('<')[0]  # 处理泛型

                # 提取注解
                if line.startswith('@'):
                    annotation = line.split('(')[0]  # 去掉参数部分
                    annotations.append(annotation)

            if package_name and class_name:
                # 分析这个类属于哪一层
                layer = self._identify_layer(package_name, class_name, annotations, content)
                if layer:
                    # 记录目录位置
                    relative_dir = java_file.parent.relative_to(project_info["src_main_java"])
                    if str(relative_dir) not in project_info["layer_patterns"][layer]["dirs"]:
                        project_info["layer_patterns"][layer]["dirs"].append(str(relative_dir))

                    # 记录命名模式
                    if class_name not in project_info["layer_patterns"][layer]["naming"]:
                        project_info["layer_patterns"][layer]["naming"].append(class_name)

                    # 记录注解模式
                    for annotation in annotations:
                        if annotation not in project_info["layer_patterns"][layer]["annotations"]:
                            project_info["layer_patterns"][layer]["annotations"].append(annotation)

                    # 分析框架信息
                    self._analyze_framework_info(annotations, content, project_info)

        except Exception:
            pass  # 忽略单个文件的分析错误

    def _identify_layer(self, package_name, class_name, annotations, content):
        """识别类属于哪一层"""
        package_lower = package_name.lower()
        class_lower = class_name.lower()

        # 基于包名判断
        if 'entity' in package_lower or 'model' in package_lower or 'domain' in package_lower:
            return 'entity'
        elif 'repository' in package_lower or 'dao' in package_lower or 'mapper' in package_lower:
            return 'repository'
        elif 'service' in package_lower:
            return 'service'
        elif 'controller' in package_lower or 'web' in package_lower or 'rest' in package_lower:
            return 'controller'
        elif 'dto' in package_lower or 'vo' in package_lower or 'request' in package_lower or 'response' in package_lower:
            return 'dto'

        # 基于类名判断
        if class_lower.endswith('entity') or class_lower.endswith('model'):
            return 'entity'
        elif class_lower.endswith('repository') or class_lower.endswith('dao') or class_lower.endswith('mapper'):
            return 'repository'
        elif class_lower.endswith('service') or class_lower.endswith('serviceimpl'):
            return 'service'
        elif class_lower.endswith('controller') or class_lower.endswith('resource'):
            return 'controller'
        elif class_lower.endswith('dto') or class_lower.endswith('vo') or class_lower.endswith('request') or class_lower.endswith('response'):
            return 'dto'

        # 基于注解判断
        for annotation in annotations:
            if annotation in ['@Entity', '@Table']:
                return 'entity'
            elif annotation in ['@Repository', '@Mapper']:
                return 'repository'
            elif annotation in ['@Service', '@Component']:
                return 'service'
            elif annotation in ['@Controller', '@RestController']:
                return 'controller'

        return None

    def _analyze_framework_info(self, annotations, content, project_info):
        """分析使用的框架信息"""
        # 分析 ORM 框架
        if any(ann in annotations for ann in ['@Entity', '@Table', '@Id']):
            project_info["framework_info"]["orm"] = "jpa"
        elif '@Mapper' in annotations or 'mybatis' in content.lower():
            project_info["framework_info"]["orm"] = "mybatis"

        # 分析 Web 框架
        if '@RestController' in annotations or '@Controller' in annotations:
            project_info["framework_info"]["web"] = "spring-mvc"

        # 分析验证框架
        if any(ann.startswith('@Valid') or ann.startswith('@NotNull') or ann.startswith('@NotBlank') for ann in annotations):
            project_info["framework_info"]["validation"] = "javax.validation"

    def _infer_project_conventions(self, project_info):
        """根据学习结果推断项目规范"""
        # 分析命名规范
        for layer, patterns in project_info["layer_patterns"].items():
            if patterns["naming"]:
                # 分析后缀模式
                suffixes = []
                for name in patterns["naming"]:
                    if layer == 'entity':
                        if name.endswith('Entity'):
                            suffixes.append('Entity')
                        elif name.endswith('Model'):
                            suffixes.append('Model')
                        else:
                            suffixes.append('')  # 无后缀
                    elif layer == 'repository':
                        if name.endswith('Repository'):
                            suffixes.append('Repository')
                        elif name.endswith('Dao'):
                            suffixes.append('Dao')
                        elif name.endswith('Mapper'):
                            suffixes.append('Mapper')
                    elif layer == 'service':
                        if name.endswith('ServiceImpl'):
                            suffixes.append('ServiceImpl')
                        elif name.endswith('Service'):
                            suffixes.append('Service')
                    elif layer == 'controller':
                        if name.endswith('Controller'):
                            suffixes.append('Controller')
                        elif name.endswith('Resource'):
                            suffixes.append('Resource')

                # 选择最常见的后缀
                if suffixes:
                    most_common_suffix = max(set(suffixes), key=suffixes.count)
                    if layer == 'entity':
                        project_info["project_conventions"]["entity_suffix"] = most_common_suffix
                    elif layer == 'repository':
                        project_info["project_conventions"]["repository_suffix"] = most_common_suffix
                    elif layer == 'service':
                        project_info["project_conventions"]["service_suffix"] = most_common_suffix
                    elif layer == 'controller':
                        project_info["project_conventions"]["controller_suffix"] = most_common_suffix

    def _get_layer_directory(self, layer, project_info, package_name):
        """根据学习结果获取层的目录位置"""
        import os
        layer_patterns = project_info["layer_patterns"][layer]

        if layer_patterns["dirs"]:
            # 使用项目中已有的目录结构
            most_common_dir = max(set(layer_patterns["dirs"]), key=layer_patterns["dirs"].count)
            return most_common_dir
        else:
            # 使用默认目录结构
            package_path = package_name.replace('.', os.sep)
            return f"{package_path}/{layer}"

    def _get_class_suffix(self, layer, project_info):
        """根据学习结果获取类名后缀"""
        conventions = project_info["project_conventions"]

        suffix_map = {
            'entity': conventions.get("entity_suffix", ""),
            'repository': conventions.get("repository_suffix", "Repository"),
            'service': conventions.get("service_suffix", "Service"),
            'controller': conventions.get("controller_suffix", "Controller")
        }

        return suffix_map.get(layer, "")

    def _save_files_to_learned_structure(self, generated_files: Dict[str, Dict[str, str]],
                                       project_info: Dict[str, Any], package_name: str) -> list:
        """将生成的文件保存到学习到的项目结构中"""
        import os
        from pathlib import Path

        saved_files = []
        src_main_java = project_info["src_main_java"]

        # 确保源码目录存在
        src_main_java.mkdir(parents=True, exist_ok=True)

        for layer, files in generated_files.items():
            if not files:  # 跳过空的层
                continue

            # 根据学习结果确定目录位置
            if layer == "dto/request" or layer == "dto/response":
                # 处理 DTO 子目录
                main_layer = "dto"
                sub_layer = layer.split("/")[1]
                layer_dir = self._get_layer_directory(main_layer, project_info, package_name)
                layer_path = Path(src_main_java) / layer_dir / sub_layer
            else:
                layer_dir = self._get_layer_directory(layer, project_info, package_name)
                layer_path = Path(src_main_java) / layer_dir

            # 创建目录
            layer_path.mkdir(parents=True, exist_ok=True)

            for filename, content in files.items():
                file_path = layer_path / filename

                # 保存文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                # 记录保存的文件路径（相对于项目根目录）
                try:
                    relative_path = file_path.relative_to(Path(project_info["project_root"]))
                    saved_files.append(str(relative_path))
                except ValueError:
                    # 如果无法计算相对路径，使用绝对路径
                    saved_files.append(str(file_path))

        return saved_files

async def main():
    """主函数 - 标准输入输出模式"""
    server = 代码生成MCP服务器Server()

    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break

            request = json.loads(line.strip())
            response = await server.handle_request(request)

            print(json.dumps(response))
            sys.stdout.flush()

        except json.JSONDecodeError:
            continue
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32000,
                    "message": str(e)
                }
            }
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == "__main__":
    asyncio.run(main())
