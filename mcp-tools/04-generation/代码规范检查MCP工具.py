#!/usr/bin/env python3
"""
代码规范检查 MCP Server
基于《代码开发规则规范》实现的代码质量检查工具
"""

import json
import os
import re
import ast
from pathlib import Path
from typing import Dict, List, Any
import subprocess

class CodeStandardChecker:
    """代码规范检查器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.violations = []
        
    def check_all_standards(self) -> Dict[str, Any]:
        """检查所有代码规范"""
        results = {
            "project_info": self._get_project_info(),
            "naming_violations": self._check_naming_conventions(),
            "architecture_violations": self._check_architecture_rules(),
            "security_violations": self._check_security_rules(),
            "documentation_violations": self._check_documentation(),
            "test_coverage": self._check_test_coverage(),
            "database_violations": self._check_database_standards(),
            "performance_issues": self._check_performance_issues(),
            # 🆕 添加业务逻辑规则检查
            # "business_logic_violations": self._check_business_logic_rules(),
            "summary": self._generate_summary()
        }
        return results
    
    def _get_project_info(self) -> Dict:
        """获取项目基本信息"""
        info = {
            "project_type": "unknown",
            "framework": "unknown",
            "language": "unknown"
        }
        
        # 检测项目类型
        if (self.project_root / "pom.xml").exists():
            info["project_type"] = "maven"
            info["language"] = "java"
            
        elif (self.project_root / "package.json").exists():
            info["project_type"] = "nodejs"
            info["language"] = "javascript"
            
        elif (self.project_root / "requirements.txt").exists():
            info["project_type"] = "python"
            info["language"] = "python"
            
        # 检测框架
        if info["language"] == "java":
            info["framework"] = self._detect_java_framework()
        elif info["language"] == "javascript":
            info["framework"] = self._detect_js_framework()
            
        return info
    
    def _check_naming_conventions(self) -> List[Dict]:
        """检查命名规范"""
        violations = []
        
        for java_file in self.project_root.rglob("*.java"):
            violations.extend(self._check_java_naming(java_file))
            
        # for py_file in self.project_root.rglob("*.py"):
        #     violations.extend(self._check_python_naming(py_file))
            
        return violations
    
    def _check_java_naming(self, file_path: Path) -> List[Dict]:
        """检查Java文件命名规范"""
        violations = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 检查类名规范 (PascalCase)
            class_pattern = r'public\s+class\s+([a-zA-Z_][a-zA-Z0-9_]*)'
            for match in re.finditer(class_pattern, content):
                class_name = match.group(1)
                if not self._is_pascal_case(class_name):
                    violations.append({
                        "file": str(file_path),
                        "line": content[:match.start()].count('\n') + 1,
                        "type": "naming_violation",
                        "rule": "类名必须使用PascalCase",
                        "violation": f"类名 '{class_name}' 不符合PascalCase规范",
                        "suggestion": f"建议改为: {self._to_pascal_case(class_name)}"
                    })
            
            # 检查方法名规范 (camelCase)
            method_pattern = r'public\s+\w+\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
            for match in re.finditer(method_pattern, content):
                method_name = match.group(1)
                if not self._is_camel_case(method_name):
                    violations.append({
                        "file": str(file_path),
                        "line": content[:match.start()].count('\n') + 1,
                        "type": "naming_violation",
                        "rule": "方法名必须使用camelCase",
                        "violation": f"方法名 '{method_name}' 不符合camelCase规范",
                        "suggestion": f"建议改为: {self._to_camel_case(method_name)}"
                    })
            
            # 检查常量命名 (UPPER_SNAKE_CASE)
            constant_pattern = r'private\s+static\s+final\s+\w+\s+([A-Z_][A-Z0-9_]*)'
            for match in re.finditer(constant_pattern, content):
                constant_name = match.group(1)
                if not self._is_upper_snake_case(constant_name):
                    violations.append({
                        "file": str(file_path),
                        "line": content[:match.start()].count('\n') + 1,
                        "type": "naming_violation",
                        "rule": "常量名必须使用UPPER_SNAKE_CASE",
                        "violation": f"常量名 '{constant_name}' 不符合UPPER_SNAKE_CASE规范",
                        "suggestion": f"建议改为: {self._to_upper_snake_case(constant_name)}"
                    })
                    
        except Exception as e:
            violations.append({
                "file": str(file_path),
                "type": "check_error",
                "error": f"检查文件时出错: {str(e)}"
            })
            
        return violations
    
    def _check_architecture_rules(self) -> List[Dict]:
        """检查架构规则"""
        violations = []
        
        # 检查分层架构
        expected_layers = ["controller", "service", "repository", "entity"]
        existing_layers = []
        
        for layer in expected_layers:
            layer_dir = self.project_root / "src" / "main" / "java" / "**" / layer
            if any(layer_dir.parent.glob(f"*{layer}*")):
                existing_layers.append(layer)
        
        missing_layers = set(expected_layers) - set(existing_layers)
        if missing_layers:
            violations.append({
                "type": "architecture_violation",
                "rule": "必须遵循分层架构",
                "violation": f"缺少以下层次: {', '.join(missing_layers)}",
                "suggestion": "请创建对应的包结构"
            })
        
        # 检查循环依赖 (暂时跳过)
        # violations.extend(self._check_circular_dependencies())
        
        return violations
    
    def _check_security_rules(self) -> List[Dict]:
        """检查安全规范"""
        violations = []
        
        for java_file in self.project_root.rglob("*.java"):
            violations.extend(self._check_java_security(java_file))
            
        return violations
    
    def _check_java_security(self, file_path: Path) -> List[Dict]:
        """检查Java安全规范"""
        violations = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查SQL注入风险
            if re.search(r'\"SELECT.*\"\s*\+', content):
                violations.append({
                    "file": str(file_path),
                    "type": "security_violation",
                    "rule": "禁止字符串拼接SQL",
                    "violation": "发现SQL字符串拼接，存在SQL注入风险",
                    "suggestion": "使用参数化查询或@Query注解"
                })
            
            # 检查输入验证
            if re.search(r'@PostMapping|@PutMapping', content):
                if not re.search(r'@Valid', content):
                    violations.append({
                        "file": str(file_path),
                        "type": "security_violation", 
                        "rule": "必须进行输入验证",
                        "violation": "POST/PUT接口缺少@Valid注解",
                        "suggestion": "在请求参数上添加@Valid注解"
                    })
                    
        except Exception as e:
            pass
            
        return violations
    
    def _check_documentation(self) -> List[Dict]:
        """检查文档规范"""
        violations = []
        
        for java_file in self.project_root.rglob("*.java"):
            violations.extend(self._check_java_documentation(java_file))
            
        return violations
    
    def _check_java_documentation(self, file_path: Path) -> List[Dict]:
        """检查Java文档规范"""
        violations = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查类级别文档
            if re.search(r'public\s+class', content):
                if not re.search(r'/\*\*.*?\*/', content, re.DOTALL):
                    violations.append({
                        "file": str(file_path),
                        "type": "documentation_violation",
                        "rule": "公共类必须有JavaDoc注释",
                        "violation": "缺少类级别的JavaDoc注释",
                        "suggestion": "添加/**...*/格式的类注释"
                    })
            
            # 检查公共方法文档
            public_methods = re.finditer(r'public\s+\w+\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', content)
            for match in public_methods:
                method_start = match.start()
                # 检查方法前是否有JavaDoc
                before_method = content[:method_start].split('\n')[-5:]  # 检查前5行
                has_javadoc = any('/**' in line for line in before_method)
                
                if not has_javadoc:
                    violations.append({
                        "file": str(file_path),
                        "line": content[:method_start].count('\n') + 1,
                        "type": "documentation_violation",
                        "rule": "公共方法必须有JavaDoc注释",
                        "violation": f"方法 '{match.group(1)}' 缺少JavaDoc注释",
                        "suggestion": "添加方法说明、参数说明、返回值说明"
                    })
                    
        except Exception as e:
            pass
            
        return violations
    
    def _check_test_coverage(self) -> Dict:
        """检查测试覆盖率"""
        coverage_info = {
            "has_tests": False,
            "test_files_count": 0,
            "coverage_percentage": 0,
            "violations": []
        }
        
        # 查找测试文件
        test_files = list(self.project_root.rglob("*Test.java"))
        test_files.extend(list(self.project_root.rglob("*test*.py")))
        
        coverage_info["test_files_count"] = len(test_files)
        coverage_info["has_tests"] = len(test_files) > 0
        
        if not coverage_info["has_tests"]:
            coverage_info["violations"].append({
                "type": "test_violation",
                "rule": "必须有测试用例",
                "violation": "项目中没有发现测试文件",
                "suggestion": "创建对应的测试类"
            })
        
        return coverage_info
    
    def _check_database_standards(self) -> List[Dict]:
        """检查数据库设计规范"""
        violations = []
        
        # 查找SQL文件或实体类
        sql_files = list(self.project_root.rglob("*.sql"))
        entity_files = []
        
        for java_file in self.project_root.rglob("*.java"):
            try:
                with open(java_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                if '@Entity' in content:
                    entity_files.append(java_file)
            except:
                pass
        
        # 检查实体类规范
        for entity_file in entity_files:
            violations.extend(self._check_entity_standards(entity_file))
            
        return violations
    
    def _check_entity_standards(self, file_path: Path) -> List[Dict]:
        """检查实体类规范"""
        violations = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否有标准字段
            required_fields = ['id', 'createdAt', 'updatedAt']
            for field in required_fields:
                if field not in content:
                    violations.append({
                        "file": str(file_path),
                        "type": "database_violation",
                        "rule": f"实体类必须包含{field}字段",
                        "violation": f"缺少标准字段: {field}",
                        "suggestion": f"添加{field}字段"
                    })
                    
        except Exception as e:
            pass
            
        return violations
    
    def _check_performance_issues(self) -> List[Dict]:
        """检查性能问题"""
        violations = []
        
        for java_file in self.project_root.rglob("*.java"):
            violations.extend(self._check_java_performance(java_file))
            
        return violations
    
    def _check_java_performance(self, file_path: Path) -> List[Dict]:
        """检查Java性能问题"""
        violations = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查N+1查询问题
            if '@OneToMany' in content and '@JoinColumn' not in content:
                violations.append({
                    "file": str(file_path),
                    "type": "performance_violation",
                    "rule": "避免N+1查询问题",
                    "violation": "@OneToMany关联可能导致N+1查询",
                    "suggestion": "使用@JoinColumn或fetch=FetchType.LAZY"
                })
            
            # 检查大数据量查询
            if 'findAll()' in content:
                violations.append({
                    "file": str(file_path),
                    "type": "performance_violation",
                    "rule": "大数据量查询必须分页",
                    "violation": "使用findAll()可能导致内存溢出",
                    "suggestion": "使用分页查询Pageable"
                })
                
        except Exception as e:
            pass
            
        return violations
    
    def _generate_summary(self) -> Dict:
        """生成检查摘要"""
        return {
            "total_violations": len(self.violations),
            "violation_types": self._count_violation_types(),
            "severity_levels": self._categorize_severity(),
            "recommendations": self._generate_recommendations()
        }
    
    # 辅助方法
    def _is_pascal_case(self, name: str) -> bool:
        return re.match(r'^[A-Z][a-zA-Z0-9]*$', name) is not None
    
    def _is_camel_case(self, name: str) -> bool:
        return re.match(r'^[a-z][a-zA-Z0-9]*$', name) is not None
    
    def _is_upper_snake_case(self, name: str) -> bool:
        return re.match(r'^[A-Z][A-Z0-9_]*$', name) is not None
    
    def _to_pascal_case(self, name: str) -> str:
        return ''.join(word.capitalize() for word in re.split(r'[_\s]+', name))
    
    def _to_camel_case(self, name: str) -> str:
        words = re.split(r'[_\s]+', name)
        return words[0].lower() + ''.join(word.capitalize() for word in words[1:])
    
    def _to_upper_snake_case(self, name: str) -> str:
        return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name).upper()

    def _check_business_logic_rules(self) -> List[Dict]:
        """检查业务逻辑规则"""
        violations = []

        # 检查发货相关业务规则
        violations.extend(self._check_shipping_business_rules())

        # 检查月初发货业务规则
        violations.extend(self._check_monthly_shipping_rules())

        # 检查商品实例相关规则
        violations.extend(self._check_product_instance_rules())

        return violations

    def _check_shipping_business_rules(self) -> List[Dict]:
        """检查发货业务规则"""
        violations = []

        # 查找发货相关的Service类
        shipping_services = []
        for java_file in self.project_root.rglob("*Service.java"):
            try:
                with open(java_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 识别发货相关的Service
                if any(keyword in content.lower() for keyword in ['shipping', 'delivery', '发货', '配送']):
                    shipping_services.append((java_file, content))
            except Exception as e:
                pass

        # 检查发货前的商品实例校验
        for java_file, content in shipping_services:
            violations.extend(self._check_product_validation_before_shipping(java_file, content))

        return violations

    def _check_product_validation_before_shipping(self, file_path: Path, content: str) -> List[Dict]:
        """检查发货前商品实例校验规则"""
        violations = []

        # 查找发货方法
        shipping_methods = re.finditer(r'public\s+\w+\s+(ship|delivery|send|发货)\w*\s*\([^)]*\)\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}', content, re.IGNORECASE | re.DOTALL)

        for match in shipping_methods:
            method_name = match.group(1)
            method_body = match.group(2)
            method_line = content[:match.start()].count('\n') + 1

            # 检查是否有商品实例校验
            validation_patterns = [
                r'validate.*product.*instance',
                r'check.*product.*valid',
                r'product.*isValid',
                r'商品.*校验',
                r'实例.*生效',
                r'validateProductInstance',
                r'checkProductStatus'
            ]

            has_validation = any(re.search(pattern, method_body, re.IGNORECASE) for pattern in validation_patterns)

            if not has_validation:
                violations.append({
                    "file": str(file_path),
                    "line": method_line,
                    "type": "business_logic_violation",
                    "rule": "发货前必须校验商品实例是否生效",
                    "violation": f"发货方法 '{method_name}' 缺少商品实例校验",
                    "suggestion": "在发货前添加商品实例生效状态校验，如: validateProductInstance(productId)"
                })

        return violations

    def _check_monthly_shipping_rules(self) -> List[Dict]:
        """检查月初发货业务规则"""
        violations = []

        # 查找月初发货相关的方法
        for java_file in self.project_root.rglob("*Service.java"):
            try:
                with open(java_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                violations.extend(self._check_monthly_sub_product_validation(java_file, content))

            except Exception as e:
                pass

        return violations

    def _check_monthly_sub_product_validation(self, file_path: Path, content: str) -> List[Dict]:
        """检查月初发货时的子产品校验"""
        violations = []

        # 查找月初发货相关方法
        monthly_shipping_patterns = [
            r'monthly.*ship',
            r'month.*delivery',
            r'月初.*发货',
            r'beginOfMonth.*ship',
            r'monthlyDelivery'
        ]

        for pattern in monthly_shipping_patterns:
            methods = re.finditer(rf'public\s+\w+\s+\w*{pattern}\w*\s*\([^)]*\)\s*\{{([^}}]*(?:\{{[^}}]*\}}[^}}]*)*)\}}', content, re.IGNORECASE | re.DOTALL)

            for match in methods:
                method_body = match.group(1)
                method_line = content[:match.start()].count('\n') + 1

                # 检查是否有子产品重复下发校验
                sub_product_validation_patterns = [
                    r'check.*sub.*product.*delivered',
                    r'validate.*monthly.*sub.*product',
                    r'已.*下发.*子产品',
                    r'当月.*子产品.*校验',
                    r'checkMonthlySubProductDelivered',
                    r'validateSubProductNotDelivered'
                ]

                has_sub_product_validation = any(re.search(val_pattern, method_body, re.IGNORECASE) for val_pattern in sub_product_validation_patterns)

                if not has_sub_product_validation:
                    violations.append({
                        "file": str(file_path),
                        "line": method_line,
                        "type": "business_logic_violation",
                        "rule": "月初发货时必须校验当月是否已经下发过子产品",
                        "violation": f"月初发货方法缺少子产品重复下发校验",
                        "suggestion": "添加子产品下发状态校验，如: checkMonthlySubProductDelivered(productId, currentMonth)"
                    })

        return violations

    def _check_product_instance_rules(self) -> List[Dict]:
        """检查商品实例相关规则"""
        violations = []

        # 查找商品实例相关的类
        for java_file in self.project_root.rglob("*Service.java"):
            try:
                with open(java_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 检查商品实例状态管理
                if any(keyword in content.lower() for keyword in ['product', 'instance', '商品', '实例']):
                    violations.extend(self._check_product_instance_status_management(java_file, content))

            except Exception as e:
                pass

        return violations

    def _check_product_instance_status_management(self, file_path: Path, content: str) -> List[Dict]:
        """检查商品实例状态管理规则"""
        violations = []

        # 查找商品实例状态变更方法
        status_change_methods = re.finditer(r'public\s+\w+\s+\w*(update|change|modify)\w*Status\w*\s*\([^)]*\)\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}', content, re.IGNORECASE | re.DOTALL)

        for match in status_change_methods:
            method_body = match.group(2)
            method_line = content[:match.start()].count('\n') + 1

            # 检查状态变更是否有业务校验
            business_validation_patterns = [
                r'validate.*business.*rule',
                r'check.*business.*condition',
                r'业务.*校验',
                r'状态.*校验',
                r'validateBusinessRule',
                r'checkStatusTransition'
            ]

            has_business_validation = any(re.search(pattern, method_body, re.IGNORECASE) for pattern in business_validation_patterns)

            if not has_business_validation:
                violations.append({
                    "file": str(file_path),
                    "line": method_line,
                    "type": "business_logic_violation",
                    "rule": "商品实例状态变更必须包含业务规则校验",
                    "violation": "状态变更方法缺少业务规则校验",
                    "suggestion": "添加业务规则校验，确保状态变更符合业务逻辑"
                })

        return violations

# MCP Server 主函数
def main():
    """MCP Server 主入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python code-standard-checker.py <project_root>")
        sys.exit(1)
    
    project_root = sys.argv[1]
    checker = CodeStandardChecker(project_root)
    results = checker.check_all_standards()
    
    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
