#!/usr/bin/env python3
"""
测试生成 MCP Server
基于生成的代码自动创建测试用例
"""

import json
import re
from typing import Dict, List, Any
from pathlib import Path

class TestGenerator:
    """测试生成器"""
    
    def __init__(self, project_root: str = "./"):
        self.project_root = Path(project_root)
        self.test_templates = self._load_test_templates()
    
    def generate_comprehensive_tests(self, generated_code: Dict[str, str], 
                                   architecture_profile: Dict[str, Any]) -> Dict[str, str]:
        """生成全面的测试用例"""
        
        test_files = {}
        
        # 为每个生成的代码文件创建对应的测试
        for file_name, code_content in generated_code.items():
            if file_name.endswith('.java'):
                test_files.update(self._generate_java_tests(file_name, code_content, architecture_profile))
        
        # 生成集成测试
        test_files.update(self._generate_integration_tests(generated_code, architecture_profile))
        
        # 生成API测试
        test_files.update(self._generate_api_tests(generated_code, architecture_profile))
        
        # 生成测试数据
        test_files.update(self._generate_test_data(generated_code))
        
        # 生成测试配置
        test_files.update(self._generate_test_configuration())
        
        return test_files
    
    def _generate_java_tests(self, file_name: str, code_content: str, 
                           architecture_profile: Dict[str, Any]) -> Dict[str, str]:
        """生成Java测试文件"""
        test_files = {}
        
        # 提取类名
        class_match = re.search(r'public\s+class\s+([A-Za-z_][A-Za-z0-9_]*)', code_content)
        if not class_match:
            return test_files
        
        class_name = class_match.group(1)
        
        # 根据类型生成不同的测试
        if 'Controller' in class_name:
            test_files[f"{class_name}Test.java"] = self._generate_controller_test(class_name, code_content)
        elif 'Service' in class_name:
            test_files[f"{class_name}Test.java"] = self._generate_service_test(class_name, code_content)
        elif 'Repository' in class_name:
            test_files[f"{class_name}Test.java"] = self._generate_repository_test(class_name, code_content)
        elif not any(keyword in class_name for keyword in ['Request', 'Response', 'DTO']):
            # 实体类测试
            test_files[f"{class_name}Test.java"] = self._generate_entity_test(class_name, code_content)
        
        return test_files
    
    def _generate_controller_test(self, class_name: str, code_content: str) -> str:
        """生成Controller测试"""
        
        # 提取包名
        package_match = re.search(r'package\s+([\w.]+);', code_content)
        package_name = package_match.group(1) if package_match else "com.example.test"
        test_package = package_name.replace('.controller', '.controller')
        
        # 提取方法
        methods = re.findall(r'@(?:Get|Post|Put|Delete)Mapping[^}]*?public\s+\w+\s+(\w+)\s*\([^)]*\)', code_content, re.DOTALL)
        
        entity_name = class_name.replace('Controller', '')
        
        test_methods = []
        for method in methods:
            test_methods.append(self._generate_controller_test_method(method, entity_name))
        
        template = f'''package {test_package};

import {package_name}.{class_name};
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * {class_name} 测试类
 * 
 * @author Test Generator
 */
@ExtendWith(MockitoExtension.class)
@WebMvcTest({class_name}.class)
class {class_name}Test {{
    
    @Mock
    private {entity_name}Service {entity_name.lower()}Service;
    
    @InjectMocks
    private {class_name} {class_name.lower()};
    
    private MockMvc mockMvc;
    private ObjectMapper objectMapper;
    
    @BeforeEach
    void setUp() {{
        mockMvc = MockMvcBuilders.standaloneSetup({class_name.lower()}).build();
        objectMapper = new ObjectMapper();
    }}
    
{chr(10).join(test_methods)}
}}'''
        
        return template
    
    def _generate_service_test(self, class_name: str, code_content: str) -> str:
        """生成Service测试"""
        
        package_match = re.search(r'package\s+([\w.]+);', code_content)
        package_name = package_match.group(1) if package_match else "com.example.test"
        
        # 提取方法
        methods = re.findall(r'public\s+\w+\s+(\w+)\s*\([^)]*\)', code_content)
        
        entity_name = class_name.replace('Service', '')
        
        test_methods = []
        for method in methods:
            test_methods.append(self._generate_service_test_method(method, entity_name))
        
        template = f'''package {package_name};

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

/**
 * {class_name} 测试类
 * 
 * @author Test Generator
 */
@ExtendWith(MockitoExtension.class)
class {class_name}Test {{
    
    @Mock
    private {entity_name}Repository {entity_name.lower()}Repository;
    
    @InjectMocks
    private {class_name} {class_name.lower()};
    
    @BeforeEach
    void setUp() {{
        // 测试数据准备
    }}
    
{chr(10).join(test_methods)}
}}'''
        
        return template
    
    def _generate_repository_test(self, class_name: str, code_content: str) -> str:
        """生成Repository测试"""
        
        package_match = re.search(r'package\s+([\w.]+);', code_content)
        package_name = package_match.group(1) if package_match else "com.example.test"
        
        entity_name = class_name.replace('Repository', '')
        
        template = f'''package {package_name};

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;

import static org.assertj.core.api.Assertions.*;

/**
 * {class_name} 测试类
 * 
 * @author Test Generator
 */
@DataJpaTest
class {class_name}Test {{
    
    @Autowired
    private TestEntityManager entityManager;
    
    @Autowired
    private {class_name} {class_name.lower()};
    
    @Test
    void testFindById_WhenEntityExists_ShouldReturnEntity() {{
        // Given
        {entity_name} {entity_name.lower()} = new {entity_name}();
        // 设置测试数据
        {entity_name} saved = entityManager.persistAndFlush({entity_name.lower()});
        
        // When
        Optional<{entity_name}> result = {class_name.lower()}.findById(saved.getId());
        
        // Then
        assertThat(result).isPresent();
        assertThat(result.get().getId()).isEqualTo(saved.getId());
    }}
    
    @Test
    void testFindById_WhenEntityNotExists_ShouldReturnEmpty() {{
        // When
        Optional<{entity_name}> result = {class_name.lower()}.findById(999L);
        
        // Then
        assertThat(result).isEmpty();
    }}
    
    @Test
    void testSave_WhenValidEntity_ShouldPersistEntity() {{
        // Given
        {entity_name} {entity_name.lower()} = new {entity_name}();
        // 设置测试数据
        
        // When
        {entity_name} saved = {class_name.lower()}.save({entity_name.lower()});
        
        // Then
        assertThat(saved.getId()).isNotNull();
        assertThat(entityManager.find({entity_name}.class, saved.getId())).isNotNull();
    }}
}}'''
        
        return template
    
    def _generate_integration_tests(self, generated_code: Dict[str, str], 
                                  architecture_profile: Dict[str, Any]) -> Dict[str, str]:
        """生成集成测试"""
        
        integration_tests = {}
        
        # 查找Controller类
        controllers = []
        for file_name, code_content in generated_code.items():
            if 'Controller' in file_name:
                class_match = re.search(r'public\s+class\s+([A-Za-z_][A-Za-z0-9_]*)', code_content)
                if class_match:
                    controllers.append(class_match.group(1))
        
        # 为每个Controller生成集成测试
        for controller in controllers:
            entity_name = controller.replace('Controller', '')
            integration_tests[f"{entity_name}IntegrationTest.java"] = self._generate_integration_test_class(entity_name)
        
        return integration_tests
    
    def _generate_integration_test_class(self, entity_name: str) -> str:
        """生成集成测试类"""
        
        template = f'''package com.example.integration;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureWebMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * {entity_name} 集成测试
 * 
 * @author Test Generator
 */
@SpringBootTest
@AutoConfigureWebMvc
@ActiveProfiles("test")
@Transactional
class {entity_name}IntegrationTest {{
    
    @Autowired
    private MockMvc mockMvc;
    
    @Autowired
    private ObjectMapper objectMapper;
    
    @Test
    void testCreate{entity_name}_WhenValidData_ShouldReturnCreated() throws Exception {{
        // Given
        Create{entity_name}Request request = new Create{entity_name}Request();
        // 设置请求数据
        
        // When & Then
        mockMvc.perform(post("/api/{entity_name.lower()}s")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").exists());
    }}
    
    @Test
    void testGet{entity_name}_WhenEntityExists_ShouldReturnEntity() throws Exception {{
        // Given - 先创建一个实体
        // 创建逻辑...
        
        // When & Then
        mockMvc.perform(get("/api/{entity_name.lower()}s/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1));
    }}
    
    @Test
    void testUpdate{entity_name}_WhenValidData_ShouldReturnUpdated() throws Exception {{
        // Given
        Update{entity_name}Request request = new Update{entity_name}Request();
        // 设置更新数据
        
        // When & Then
        mockMvc.perform(put("/api/{entity_name.lower()}s/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk());
    }}
    
    @Test
    void testDelete{entity_name}_WhenEntityExists_ShouldReturnOk() throws Exception {{
        // When & Then
        mockMvc.perform(delete("/api/{entity_name.lower()}s/1"))
                .andExpect(status().isOk());
    }}
    
    @Test
    void testGetAll{entity_name}s_ShouldReturnPagedResult() throws Exception {{
        // When & Then
        mockMvc.perform(get("/api/{entity_name.lower()}s")
                .param("page", "0")
                .param("size", "10"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content").isArray());
    }}
}}'''
        
        return template
    
    def _generate_test_data(self, generated_code: Dict[str, str]) -> Dict[str, str]:
        """生成测试数据"""
        
        test_data_files = {}
        
        # 生成测试数据工厂
        test_data_files["TestDataFactory.java"] = '''package com.example.testdata;

import java.time.LocalDateTime;
import java.util.Random;

/**
 * 测试数据工厂
 * 
 * @author Test Generator
 */
public class TestDataFactory {
    
    private static final Random random = new Random();
    
    public static User createTestUser() {
        User user = new User();
        user.setUsername("testuser" + random.nextInt(1000));
        user.setEmail("test" + random.nextInt(1000) + "@example.com");
        user.setCreatedAt(LocalDateTime.now());
        user.setUpdatedAt(LocalDateTime.now());
        return user;
    }
    
    public static CreateUserRequest createUserRequest() {
        CreateUserRequest request = new CreateUserRequest();
        request.setUsername("testuser" + random.nextInt(1000));
        request.setEmail("test" + random.nextInt(1000) + "@example.com");
        return request;
    }
}'''
        
        return test_data_files
    
    def _generate_test_configuration(self) -> Dict[str, str]:
        """生成测试配置"""
        
        config_files = {}
        
        # 测试配置文件
        config_files["application-test.yml"] = '''spring:
  datasource:
    url: jdbc:h2:mem:testdb
    driver-class-name: org.h2.Driver
    username: sa
    password: 
  jpa:
    hibernate:
      ddl-auto: create-drop
    show-sql: true
  h2:
    console:
      enabled: true

logging:
  level:
    com.example: DEBUG
    org.springframework.web: DEBUG
'''
        
        return config_files
    
    # 辅助方法
    def _generate_controller_test_method(self, method_name: str, entity_name: str) -> str:
        """生成Controller测试方法"""
        
        if method_name.startswith('get') and 'ById' in method_name:
            return f'''    
    @Test
    void test{method_name.capitalize()}_WhenEntityExists_ShouldReturnEntity() throws Exception {{
        // Given
        {entity_name} {entity_name.lower()} = new {entity_name}();
        when({entity_name.lower()}Service.findById(1L)).thenReturn({entity_name.lower()});
        
        // When & Then
        mockMvc.perform(get("/api/{entity_name.lower()}s/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").exists());
    }}'''
        
        elif method_name.startswith('create') or method_name.startswith('post'):
            return f'''    
    @Test
    void test{method_name.capitalize()}_WhenValidData_ShouldReturnCreated() throws Exception {{
        // Given
        Create{entity_name}Request request = new Create{entity_name}Request();
        {entity_name} {entity_name.lower()} = new {entity_name}();
        when({entity_name.lower()}Service.create(any())).thenReturn({entity_name.lower()});
        
        // When & Then
        mockMvc.perform(post("/api/{entity_name.lower()}s")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk());
    }}'''
        
        return f'''    
    @Test
    void test{method_name.capitalize()}_ShouldWork() throws Exception {{
        // TODO: 实现 {method_name} 的测试逻辑
    }}'''
    
    def _generate_service_test_method(self, method_name: str, entity_name: str) -> str:
        """生成Service测试方法"""
        
        if 'findById' in method_name:
            return f'''    
    @Test
    void test{method_name.capitalize()}_WhenEntityExists_ShouldReturnEntity() {{
        // Given
        Long id = 1L;
        {entity_name} expected = new {entity_name}();
        when({entity_name.lower()}Repository.findById(id)).thenReturn(Optional.of(expected));
        
        // When
        {entity_name} result = {entity_name.lower()}Service.{method_name}(id);
        
        // Then
        assertThat(result).isEqualTo(expected);
    }}'''
        
        elif 'create' in method_name or 'save' in method_name:
            return f'''    
    @Test
    void test{method_name.capitalize()}_WhenValidEntity_ShouldReturnSavedEntity() {{
        // Given
        {entity_name} {entity_name.lower()} = new {entity_name}();
        when({entity_name.lower()}Repository.save({entity_name.lower()})).thenReturn({entity_name.lower()});
        
        // When
        {entity_name} result = {entity_name.lower()}Service.{method_name}({entity_name.lower()});
        
        // Then
        assertThat(result).isEqualTo({entity_name.lower()});
        verify({entity_name.lower()}Repository).save({entity_name.lower()});
    }}'''
        
        return f'''    
    @Test
    void test{method_name.capitalize()}_ShouldWork() {{
        // TODO: 实现 {method_name} 的测试逻辑
    }}'''
    
    def _load_test_templates(self) -> Dict[str, str]:
        """加载测试模板"""
        return {}

# MCP Server 主函数
def main():
    """MCP Server 主入口"""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python 测试生成MCP工具.py <generated_code_json> <architecture_profile_json>")
        sys.exit(1)
    
    generated_code_json = sys.argv[1]
    architecture_profile_json = sys.argv[2]
    
    try:
        generated_code = json.loads(generated_code_json)
        architecture_profile = json.loads(architecture_profile_json)
    except json.JSONDecodeError:
        print("Invalid JSON format")
        sys.exit(1)
    
    generator = TestGenerator()
    test_files = generator.generate_comprehensive_tests(generated_code, architecture_profile)
    
    print(json.dumps(test_files, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
