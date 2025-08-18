#!/usr/bin/env python3
"""
用户故事生成 MCP Server
基于需求分析结果生成用户故事和验收标准
"""

import json
from typing import Dict, List, Any

class UserStoryGenerator:
    """用户故事生成器"""
    
    def __init__(self):
        self.story_templates = self._load_story_templates()
    
    def generate_user_stories(self, requirements_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """生成用户故事"""
        user_stories = []
        
        functional_reqs = requirements_analysis.get("functional_requirements", [])
        user_roles = requirements_analysis.get("user_roles", [])
        data_entities = requirements_analysis.get("data_entities", [])
        
        # 为每个功能需求生成用户故事
        for req in functional_reqs:
            stories = self._generate_stories_for_requirement(req, user_roles, data_entities)
            user_stories.extend(stories)
        
        # 为每个数据实体生成CRUD用户故事
        for entity in data_entities:
            crud_stories = self._generate_crud_stories(entity, user_roles)
            user_stories.extend(crud_stories)
        
        return user_stories
    
    def _generate_stories_for_requirement(self, requirement: Dict[str, str], 
                                        user_roles: List[Dict[str, str]], 
                                        data_entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """为功能需求生成用户故事"""
        stories = []
        
        req_desc = requirement["description"]
        
        # 确定相关的用户角色
        relevant_roles = self._find_relevant_roles(req_desc, user_roles)
        if not relevant_roles:
            relevant_roles = [{"name": "用户", "description": "系统用户"}]
        
        # 为每个相关角色生成故事
        for role in relevant_roles:
            story = {
                "id": f"US-{len(stories) + 1:03d}",
                "title": self._generate_story_title(req_desc),
                "as_a": role["name"],
                "i_want": self._extract_want_statement(req_desc),
                "so_that": self._generate_benefit_statement(req_desc),
                "priority": requirement.get("priority", "中"),
                "story_points": self._estimate_story_points(requirement.get("complexity", "中")),
                "acceptance_criteria": self._generate_acceptance_criteria(req_desc),
                "definition_of_done": self._generate_definition_of_done(),
                "dependencies": [],
                "tags": self._generate_tags(req_desc)
            }
            stories.append(story)
        
        return stories
    
    def _generate_crud_stories(self, entity: Dict[str, Any], 
                             user_roles: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """为数据实体生成CRUD用户故事"""
        stories = []
        entity_name = entity["name"]
        
        # 确定能操作此实体的角色
        relevant_roles = self._find_entity_roles(entity_name, user_roles)
        if not relevant_roles:
            relevant_roles = [{"name": "管理员", "description": "系统管理员"}]
        
        crud_operations = [
            {
                "operation": "创建",
                "want": f"创建新的{entity_name}",
                "benefit": f"能够添加{entity_name}信息到系统中"
            },
            {
                "operation": "查看",
                "want": f"查看{entity_name}详情",
                "benefit": f"能够了解{entity_name}的具体信息"
            },
            {
                "operation": "更新",
                "want": f"修改{entity_name}信息",
                "benefit": f"能够保持{entity_name}信息的准确性"
            },
            {
                "operation": "删除",
                "want": f"删除{entity_name}",
                "benefit": f"能够移除不需要的{entity_name}信息"
            },
            {
                "operation": "列表查询",
                "want": f"查看{entity_name}列表",
                "benefit": f"能够浏览所有{entity_name}信息"
            }
        ]
        
        for role in relevant_roles:
            for op in crud_operations:
                story = {
                    "id": f"US-CRUD-{entity_name}-{op['operation']}-{len(stories) + 1:02d}",
                    "title": f"{role['name']}{op['operation']}{entity_name}",
                    "as_a": role["name"],
                    "i_want": op["want"],
                    "so_that": op["benefit"],
                    "priority": "中",
                    "story_points": self._estimate_crud_story_points(op["operation"]),
                    "acceptance_criteria": self._generate_crud_acceptance_criteria(entity_name, op["operation"]),
                    "definition_of_done": self._generate_definition_of_done(),
                    "dependencies": [],
                    "tags": ["CRUD", entity_name, op["operation"]]
                }
                stories.append(story)
        
        return stories
    
    def _generate_acceptance_criteria(self, requirement_desc: str) -> List[str]:
        """生成验收标准"""
        criteria = []
        
        # 基本验收标准模板
        criteria.append("功能按照需求描述正确实现")
        criteria.append("界面友好，操作简单直观")
        criteria.append("数据验证正确，错误提示清晰")
        criteria.append("响应时间在可接受范围内")
        
        # 根据需求内容添加特定标准
        if "查询" in requirement_desc:
            criteria.append("查询结果准确，支持分页显示")
            criteria.append("支持常用的筛选和排序功能")
        
        if "创建" in requirement_desc or "添加" in requirement_desc:
            criteria.append("必填字段验证正确")
            criteria.append("创建成功后给出明确提示")
        
        if "修改" in requirement_desc or "更新" in requirement_desc:
            criteria.append("只能修改有权限的数据")
            criteria.append("修改前显示当前值")
        
        if "删除" in requirement_desc:
            criteria.append("删除前需要确认操作")
            criteria.append("不能删除被引用的数据")
        
        return criteria
    
    def _generate_crud_acceptance_criteria(self, entity_name: str, operation: str) -> List[str]:
        """生成CRUD操作的验收标准"""
        criteria = []
        
        if operation == "创建":
            criteria.extend([
                f"能够成功创建{entity_name}记录",
                "必填字段验证正确",
                "数据格式验证正确",
                "创建成功后跳转到详情页面",
                "创建失败时显示错误信息"
            ])
        
        elif operation == "查看":
            criteria.extend([
                f"能够正确显示{entity_name}详细信息",
                "所有字段显示完整",
                "格式化显示友好",
                "不存在的记录显示404错误"
            ])
        
        elif operation == "更新":
            criteria.extend([
                f"能够成功更新{entity_name}信息",
                "更新前显示当前值",
                "字段验证正确",
                "更新成功后显示最新信息",
                "并发更新冲突处理正确"
            ])
        
        elif operation == "删除":
            criteria.extend([
                f"能够成功删除{entity_name}记录",
                "删除前需要确认操作",
                "删除后从列表中移除",
                "被引用的记录不能删除",
                "删除操作记录日志"
            ])
        
        elif operation == "列表查询":
            criteria.extend([
                f"能够正确显示{entity_name}列表",
                "支持分页显示",
                "支持基本筛选功能",
                "支持排序功能",
                "空列表时显示友好提示"
            ])
        
        return criteria
    
    def _generate_definition_of_done(self) -> List[str]:
        """生成完成定义"""
        return [
            "代码开发完成并通过代码审查",
            "单元测试编写完成且通过",
            "集成测试通过",
            "用户界面符合设计规范",
            "功能测试通过",
            "文档更新完成",
            "部署到测试环境验证通过"
        ]
    
    def generate_sprint_plan(self, user_stories: List[Dict[str, Any]], 
                           sprint_capacity: int = 20) -> List[Dict[str, Any]]:
        """生成Sprint计划"""
        sprints = []
        current_sprint = {
            "sprint_number": 1,
            "capacity": sprint_capacity,
            "current_points": 0,
            "stories": []
        }
        
        # 按优先级排序用户故事
        sorted_stories = sorted(user_stories, key=lambda x: self._priority_weight(x["priority"]), reverse=True)
        
        for story in sorted_stories:
            story_points = story["story_points"]
            
            # 检查当前Sprint是否还能容纳这个故事
            if current_sprint["current_points"] + story_points <= sprint_capacity:
                current_sprint["stories"].append(story)
                current_sprint["current_points"] += story_points
            else:
                # 开始新的Sprint
                sprints.append(current_sprint.copy())
                current_sprint = {
                    "sprint_number": len(sprints) + 1,
                    "capacity": sprint_capacity,
                    "current_points": story_points,
                    "stories": [story]
                }
        
        # 添加最后一个Sprint
        if current_sprint["stories"]:
            sprints.append(current_sprint)
        
        return sprints
    
    # 辅助方法
    def _load_story_templates(self) -> Dict[str, str]:
        """加载用户故事模板"""
        return {
            "basic": "作为{role}，我希望{want}，以便{benefit}",
            "detailed": "作为{role}，我希望能够{want}，这样我就可以{benefit}，从而{value}"
        }
    
    def _find_relevant_roles(self, requirement_desc: str, user_roles: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """查找相关的用户角色"""
        relevant_roles = []
        
        for role in user_roles:
            if role["name"] in requirement_desc:
                relevant_roles.append(role)
        
        return relevant_roles
    
    def _find_entity_roles(self, entity_name: str, user_roles: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """查找能操作实体的角色"""
        # 简单逻辑：管理员可以操作所有实体，其他角色根据名称匹配
        relevant_roles = []
        
        for role in user_roles:
            if "管理员" in role["name"] or entity_name in role["name"]:
                relevant_roles.append(role)
        
        return relevant_roles
    
    def _estimate_story_points(self, complexity: str) -> int:
        """估算故事点数"""
        complexity_points = {
            "低": 2,
            "中": 5,
            "高": 8
        }
        return complexity_points.get(complexity, 5)
    
    def _estimate_crud_story_points(self, operation: str) -> int:
        """估算CRUD操作的故事点数"""
        operation_points = {
            "创建": 3,
            "查看": 2,
            "更新": 3,
            "删除": 2,
            "列表查询": 3
        }
        return operation_points.get(operation, 3)
    
    def _priority_weight(self, priority: str) -> int:
        """优先级权重"""
        weights = {"高": 3, "中": 2, "低": 1}
        return weights.get(priority, 2)

# MCP Server 主函数
def main():
    """MCP Server 主入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python 用户故事生成MCP工具.py <requirements_analysis_json>")
        sys.exit(1)
    
    requirements_analysis_json = sys.argv[1]
    
    try:
        requirements_analysis = json.loads(requirements_analysis_json)
    except json.JSONDecodeError:
        print("Invalid requirements analysis JSON format")
        sys.exit(1)
    
    generator = UserStoryGenerator()
    
    # 生成用户故事
    user_stories = generator.generate_user_stories(requirements_analysis)
    
    # 生成Sprint计划
    sprint_plan = generator.generate_sprint_plan(user_stories)
    
    result = {
        "user_stories": user_stories,
        "sprint_plan": sprint_plan,
        "summary": {
            "total_stories": len(user_stories),
            "total_sprints": len(sprint_plan),
            "total_story_points": sum(story["story_points"] for story in user_stories)
        }
    }
    
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
