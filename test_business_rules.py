#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path
import re
import json

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class BusinessRuleChecker:
    """业务规则检查器 - 简化版本专门用于测试"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
    
    def check_business_logic_rules(self):
        """检查业务逻辑规则"""
        violations = []
        
        # 检查发货相关业务规则
        violations.extend(self._check_shipping_business_rules())
        
        # 检查月初发货业务规则
        violations.extend(self._check_monthly_shipping_rules())
        
        # 检查商品实例相关规则
        violations.extend(self._check_product_instance_rules())
        
        return violations
    
    def _check_shipping_business_rules(self):
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
    
    def _check_product_validation_before_shipping(self, file_path, content):
        """检查发货前商品实例校验规则"""
        violations = []
        
        # 查找发货方法 - 修复正则表达式
        shipping_methods = re.finditer(r'public\s+\w+\s+(\w*(?:ship|delivery|send|发货)\w*)\s*\([^)]*\)\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', content, re.IGNORECASE | re.DOTALL)
        
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
    
    def _check_monthly_shipping_rules(self):
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
    
    def _check_monthly_sub_product_validation(self, file_path, content):
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
    
    def _check_product_instance_rules(self):
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
    
    def _check_product_instance_status_management(self, file_path, content):
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

def main():
    """测试业务规则检查"""
    if len(sys.argv) < 2:
        print("Usage: python test_business_rules.py <project_root>")
        sys.exit(1)
    
    project_root = sys.argv[1]
    checker = BusinessRuleChecker(project_root)
    violations = checker.check_business_logic_rules()
    
    print("🔍 业务规则检查结果:")
    print("=" * 50)
    
    if not violations:
        print("✅ 未发现业务规则违规")
    else:
        print(f"❌ 发现 {len(violations)} 个业务规则违规:")
        print()
        
        for i, violation in enumerate(violations, 1):
            print(f"{i}. 文件: {violation['file']}")
            if 'line' in violation:
                print(f"   行号: {violation['line']}")
            print(f"   规则: {violation['rule']}")
            print(f"   违规: {violation['violation']}")
            print(f"   建议: {violation['suggestion']}")
            print("-" * 40)
    
    # 输出JSON格式结果
    result = {
        "business_logic_violations": violations,
        "summary": {
            "total_violations": len(violations),
            "violation_types": {}
        }
    }
    
    # 统计违规类型
    for violation in violations:
        rule = violation['rule']
        if rule not in result['summary']['violation_types']:
            result['summary']['violation_types'][rule] = 0
        result['summary']['violation_types'][rule] += 1
    
    print("\n📊 JSON格式结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
