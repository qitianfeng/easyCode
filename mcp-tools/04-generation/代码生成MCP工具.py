#!/usr/bin/env python3
"""
代码生成 MCP Server
基于《代码开发规则规范》生成符合规范的代码
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

class CodeGenerator:
    """代码生成器"""
    
    def __init__(self, project_root: str, project_info: Dict = None):
        self.project_root = Path(project_root)
        self.project_info = project_info or {}
        self.templates = self._load_templates()
    
    def generate_crud_module(self, entity_name: str, fields: List[Dict]) -> Dict[str, str]:
        """生成完整的CRUD模块"""
        generated_files = {}
        
        # 生成实体类
        generated_files[f"{entity_name}.java"] = self._generate_entity(entity_name, fields)
        
        # 生成Repository接口
        generated_files[f"{entity_name}Repository.java"] = self._generate_repository(entity_name)
        
        # 生成Service类
        generated_files[f"{entity_name}Service.java"] = self._generate_service(entity_name)
        
        # 生成Controller类
        generated_files[f"{entity_name}Controller.java"] = self._generate_controller(entity_name)
        
        # 生成DTO类
        generated_files[f"Create{entity_name}Request.java"] = self._generate_create_dto(entity_name, fields)
        generated_files[f"Update{entity_name}Request.java"] = self._generate_update_dto(entity_name, fields)
        generated_files[f"{entity_name}Response.java"] = self._generate_response_dto(entity_name, fields)
        
        # 生成测试类
        generated_files[f"{entity_name}ServiceTest.java"] = self._generate_service_test(entity_name)
        generated_files[f"{entity_name}ControllerTest.java"] = self._generate_controller_test(entity_name)
        
        # 生成数据库脚本
        generated_files[f"create_{entity_name.lower()}_table.sql"] = self._generate_sql_script(entity_name, fields)
        
        return generated_files
    
    def _generate_entity(self, entity_name: str, fields: List[Dict]) -> str:
        """生成实体类"""
        package_name = self._get_package_name("entity")
        
        template = f'''package {package_name};

import javax.persistence.*;
import javax.validation.constraints.*;
import java.time.LocalDateTime;
import java.util.Objects;

/**
 * {entity_name}实体类
 * 
 * @author {self._get_author()}
 * @since {self._get_version()}
 */
@Entity
@Table(name = "{self._to_snake_case(entity_name)}s")
public class {entity_name} {{
    
    /**
     * 主键ID
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
{self._generate_entity_fields(fields)}
    
    /**
     * 创建时间
     */
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    /**
     * 更新时间
     */
    @Column(name = "updated_at", nullable = false)
    private LocalDateTime updatedAt;
    
    /**
     * 创建人ID
     */
    @Column(name = "created_by")
    private Long createdBy;
    
    /**
     * 更新人ID
     */
    @Column(name = "updated_by")
    private Long updatedBy;
    
    /**
     * 版本号（乐观锁）
     */
    @Version
    private Integer version;
    
    /**
     * 逻辑删除标记
     */
    @Column(name = "deleted")
    private Boolean deleted = false;
    
    /**
     * JPA生命周期回调
     */
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
    
    @Override
    public String toString() {{
        return "{entity_name}{{" +
                "id=" + id +
                ", createdAt=" + createdAt +
                ", updatedAt=" + updatedAt +
                "}}";
    }}
}}'''
        return template
    
    def _generate_repository(self, entity_name: str) -> str:
        """生成Repository接口"""
        package_name = self._get_package_name("repository")
        entity_package = self._get_package_name("entity")
        
        template = f'''package {package_name};

import {entity_package}.{entity_name};
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * {entity_name}数据访问接口
 * 
 * @author {self._get_author()}
 * @since {self._get_version()}
 */
@Repository
public interface {entity_name}Repository extends JpaRepository<{entity_name}, Long> {{
    
    /**
     * 根据ID查找未删除的记录
     * 
     * @param id 主键ID
     * @return {entity_name}对象
     */
    @Query("SELECT e FROM {entity_name} e WHERE e.id = :id AND e.deleted = false")
    Optional<{entity_name}> findByIdAndNotDeleted(@Param("id") Long id);
    
    /**
     * 查找所有未删除的记录（分页）
     * 
     * @param pageable 分页参数
     * @return 分页结果
     */
    @Query("SELECT e FROM {entity_name} e WHERE e.deleted = false")
    Page<{entity_name}> findAllNotDeleted(Pageable pageable);
    
    /**
     * 逻辑删除
     * 
     * @param id 主键ID
     */
    @Query("UPDATE {entity_name} e SET e.deleted = true WHERE e.id = :id")
    void softDeleteById(@Param("id") Long id);
}}'''
        return template
    
    def _generate_service(self, entity_name: str) -> str:
        """生成Service类"""
        package_name = self._get_package_name("service")
        entity_package = self._get_package_name("entity")
        repository_package = self._get_package_name("repository")
        
        template = f'''package {package_name};

import {entity_package}.{entity_name};
import {repository_package}.{entity_name}Repository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

/**
 * {entity_name}业务逻辑服务
 * 
 * @author {self._get_author()}
 * @since {self._get_version()}
 */
@Service
@Transactional
public class {entity_name}Service {{
    
    private final {entity_name}Repository {entity_name.lower()}Repository;
    
    @Autowired
    public {entity_name}Service({entity_name}Repository {entity_name.lower()}Repository) {{
        this.{entity_name.lower()}Repository = {entity_name.lower()}Repository;
    }}
    
    /**
     * 创建{entity_name}
     * 
     * @param {entity_name.lower()} {entity_name}对象
     * @return 保存后的{entity_name}对象
     * @throws IllegalArgumentException 当参数为null时抛出
     */
    public {entity_name} create({entity_name} {entity_name.lower()}) {{
        if ({entity_name.lower()} == null) {{
            throw new IllegalArgumentException("{entity_name}对象不能为空");
        }}
        
        // 业务逻辑验证
        validateForCreate({entity_name.lower()});
        
        return {entity_name.lower()}Repository.save({entity_name.lower()});
    }}
    
    /**
     * 根据ID查找{entity_name}
     * 
     * @param id 主键ID
     * @return {entity_name}对象，如果不存在返回null
     * @throws IllegalArgumentException 当id为null时抛出
     */
    @Transactional(readOnly = true)
    public {entity_name} findById(Long id) {{
        if (id == null) {{
            throw new IllegalArgumentException("ID不能为空");
        }}
        
        return {entity_name.lower()}Repository.findByIdAndNotDeleted(id).orElse(null);
    }}
    
    /**
     * 分页查询{entity_name}
     * 
     * @param pageable 分页参数
     * @return 分页结果
     */
    @Transactional(readOnly = true)
    public Page<{entity_name}> findAll(Pageable pageable) {{
        return {entity_name.lower()}Repository.findAllNotDeleted(pageable);
    }}
    
    /**
     * 更新{entity_name}
     * 
     * @param {entity_name.lower()} {entity_name}对象
     * @return 更新后的{entity_name}对象
     * @throws IllegalArgumentException 当参数为null或ID为null时抛出
     */
    public {entity_name} update({entity_name} {entity_name.lower()}) {{
        if ({entity_name.lower()} == null || {entity_name.lower()}.getId() == null) {{
            throw new IllegalArgumentException("{entity_name}对象或ID不能为空");
        }}
        
        // 检查记录是否存在
        {entity_name} existing = findById({entity_name.lower()}.getId());
        if (existing == null) {{
            throw new IllegalArgumentException("要更新的{entity_name}不存在");
        }}
        
        // 业务逻辑验证
        validateForUpdate({entity_name.lower()});
        
        return {entity_name.lower()}Repository.save({entity_name.lower()});
    }}
    
    /**
     * 删除{entity_name}（逻辑删除）
     * 
     * @param id 主键ID
     * @throws IllegalArgumentException 当id为null时抛出
     */
    public void deleteById(Long id) {{
        if (id == null) {{
            throw new IllegalArgumentException("ID不能为空");
        }}
        
        // 检查记录是否存在
        {entity_name} existing = findById(id);
        if (existing == null) {{
            throw new IllegalArgumentException("要删除的{entity_name}不存在");
        }}
        
        {entity_name.lower()}Repository.softDeleteById(id);
    }}
    
    /**
     * 创建时的业务逻辑验证
     * 
     * @param {entity_name.lower()} {entity_name}对象
     */
    private void validateForCreate({entity_name} {entity_name.lower()}) {{
        // TODO: 添加创建时的业务逻辑验证
    }}
    
    /**
     * 更新时的业务逻辑验证
     * 
     * @param {entity_name.lower()} {entity_name}对象
     */
    private void validateForUpdate({entity_name} {entity_name.lower()}) {{
        // TODO: 添加更新时的业务逻辑验证
    }}
}}'''
        return template
    
    def _generate_controller(self, entity_name: str) -> str:
        """生成Controller类"""
        package_name = self._get_package_name("controller")
        service_package = self._get_package_name("service")
        entity_package = self._get_package_name("entity")
        
        template = f'''package {package_name};

import {entity_package}.{entity_name};
import {service_package}.{entity_name}Service;
import io.swagger.annotations.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;

/**
 * {entity_name}控制器
 * 
 * @author {self._get_author()}
 * @since {self._get_version()}
 */
@RestController
@RequestMapping("/api/{entity_name.lower()}s")
@Api(tags = "{entity_name}管理", description = "{entity_name}相关操作接口")
public class {entity_name}Controller {{
    
    private final {entity_name}Service {entity_name.lower()}Service;
    
    @Autowired
    public {entity_name}Controller({entity_name}Service {entity_name.lower()}Service) {{
        this.{entity_name.lower()}Service = {entity_name.lower()}Service;
    }}
    
    /**
     * 创建{entity_name}
     * 
     * @param request 创建请求
     * @return 创建的{entity_name}对象
     */
    @PostMapping
    @ApiOperation(value = "创建{entity_name}", notes = "创建新的{entity_name}记录")
    @ApiResponses({{
        @ApiResponse(code = 200, message = "创建成功"),
        @ApiResponse(code = 400, message = "请求参数错误"),
        @ApiResponse(code = 500, message = "服务器错误")
    }})
    @PreAuthorize("hasRole('ADMIN') or hasPermission(null, '{entity_name}', 'CREATE')")
    public ResponseEntity<{entity_name}> create(
        @ApiParam(value = "创建{entity_name}请求", required = true)
        @Valid @RequestBody Create{entity_name}Request request
    ) {{
        {entity_name} {entity_name.lower()} = convertToEntity(request);
        {entity_name} created = {entity_name.lower()}Service.create({entity_name.lower()});
        return ResponseEntity.ok(created);
    }}
    
    /**
     * 根据ID获取{entity_name}
     * 
     * @param id {entity_name}ID
     * @return {entity_name}对象
     */
    @GetMapping("/{{id}}")
    @ApiOperation(value = "根据ID获取{entity_name}", notes = "返回{entity_name}详细信息")
    @PreAuthorize("hasRole('ADMIN') or hasPermission(#id, '{entity_name}', 'READ')")
    public ResponseEntity<{entity_name}> getById(
        @ApiParam(value = "{entity_name}ID", required = true)
        @PathVariable Long id
    ) {{
        {entity_name} {entity_name.lower()} = {entity_name.lower()}Service.findById(id);
        if ({entity_name.lower()} == null) {{
            return ResponseEntity.notFound().build();
        }}
        return ResponseEntity.ok({entity_name.lower()});
    }}
    
    /**
     * 分页查询{entity_name}
     * 
     * @param pageable 分页参数
     * @return 分页结果
     */
    @GetMapping
    @ApiOperation(value = "分页查询{entity_name}", notes = "返回{entity_name}分页列表")
    @PreAuthorize("hasRole('USER')")
    public ResponseEntity<Page<{entity_name}>> getAll(Pageable pageable) {{
        Page<{entity_name}> page = {entity_name.lower()}Service.findAll(pageable);
        return ResponseEntity.ok(page);
    }}
    
    /**
     * 更新{entity_name}
     * 
     * @param id {entity_name}ID
     * @param request 更新请求
     * @return 更新后的{entity_name}对象
     */
    @PutMapping("/{{id}}")
    @ApiOperation(value = "更新{entity_name}", notes = "更新指定的{entity_name}记录")
    @PreAuthorize("hasRole('ADMIN') or hasPermission(#id, '{entity_name}', 'UPDATE')")
    public ResponseEntity<{entity_name}> update(
        @ApiParam(value = "{entity_name}ID", required = true) @PathVariable Long id,
        @ApiParam(value = "更新{entity_name}请求", required = true)
        @Valid @RequestBody Update{entity_name}Request request
    ) {{
        {entity_name} {entity_name.lower()} = convertToEntity(request);
        {entity_name.lower()}.setId(id);
        {entity_name} updated = {entity_name.lower()}Service.update({entity_name.lower()});
        return ResponseEntity.ok(updated);
    }}
    
    /**
     * 删除{entity_name}
     * 
     * @param id {entity_name}ID
     * @return 删除结果
     */
    @DeleteMapping("/{{id}}")
    @ApiOperation(value = "删除{entity_name}", notes = "逻辑删除指定的{entity_name}记录")
    @PreAuthorize("hasRole('ADMIN') or hasPermission(#id, '{entity_name}', 'DELETE')")
    public ResponseEntity<Void> delete(
        @ApiParam(value = "{entity_name}ID", required = true) @PathVariable Long id
    ) {{
        {entity_name.lower()}Service.deleteById(id);
        return ResponseEntity.ok().build();
    }}
    
    /**
     * 将创建请求转换为实体对象
     * 
     * @param request 创建请求
     * @return 实体对象
     */
    private {entity_name} convertToEntity(Create{entity_name}Request request) {{
        // TODO: 实现请求到实体的转换逻辑
        return new {entity_name}();
    }}
    
    /**
     * 将更新请求转换为实体对象
     * 
     * @param request 更新请求
     * @return 实体对象
     */
    private {entity_name} convertToEntity(Update{entity_name}Request request) {{
        // TODO: 实现请求到实体的转换逻辑
        return new {entity_name}();
    }}
}}'''
        return template
    
    # 辅助方法
    def _load_templates(self) -> Dict:
        """加载代码模板"""
        return {}
    
    def _get_package_name(self, layer: str) -> str:
        """获取包名"""
        base_package = self.project_info.get("base_package", "com.example.project")
        return f"{base_package}.{layer}"
    
    def _get_author(self) -> str:
        """获取作者信息"""
        return self.project_info.get("author", "System Generated")
    
    def _get_version(self) -> str:
        """获取版本信息"""
        return self.project_info.get("version", "1.0.0")
    
    def _to_snake_case(self, name: str) -> str:
        """转换为snake_case"""
        import re
        return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name).lower()
    
    def _generate_entity_fields(self, fields: List[Dict]) -> str:
        """生成实体字段"""
        field_code = ""
        for field in fields:
            field_code += f'''    
    /**
     * {field.get('comment', field['name'])}
     */
    @Column(name = "{self._to_snake_case(field['name'])}")
    private {field['type']} {field['name']};
'''
        return field_code
    
    def _generate_getters_setters(self, entity_name: str, fields: List[Dict]) -> str:
        """生成getter和setter方法"""
        code = ""
        
        # 标准字段的getter/setter
        standard_fields = [
            {"name": "id", "type": "Long"},
            {"name": "createdAt", "type": "LocalDateTime"},
            {"name": "updatedAt", "type": "LocalDateTime"},
            {"name": "createdBy", "type": "Long"},
            {"name": "updatedBy", "type": "Long"},
            {"name": "version", "type": "Integer"},
            {"name": "deleted", "type": "Boolean"}
        ]
        
        all_fields = fields + standard_fields
        
        for field in all_fields:
            field_name = field['name']
            field_type = field['type']
            capitalized_name = field_name.capitalize()
            
            # Getter
            code += f'''    
    public {field_type} get{capitalized_name}() {{
        return {field_name};
    }}
    
    public void set{capitalized_name}({field_type} {field_name}) {{
        this.{field_name} = {field_name};
    }}
'''
        
        return code

# MCP Server 主函数
def main():
    """MCP Server 主入口"""
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python code-generator.py <project_root> <entity_name> <fields_json>")
        sys.exit(1)
    
    project_root = sys.argv[1]
    entity_name = sys.argv[2]
    fields_json = sys.argv[3]
    
    try:
        fields = json.loads(fields_json)
    except json.JSONDecodeError:
        print("Invalid fields JSON format")
        sys.exit(1)
    
    generator = CodeGenerator(project_root)
    generated_files = generator.generate_crud_module(entity_name, fields)
    
    print(json.dumps(generated_files, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
