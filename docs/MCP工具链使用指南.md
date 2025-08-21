# MCP 工具链使用指南

## 🎯 概述

这是一套完整的软件开发流程 MCP (Model Context Protocol) 工具链，支持从产品需求分析到代码测试的全流程开发。核心特色是**智能架构识别**，能够识别现有项目架构并生成完全匹配的代码。

## 📋 配置文件说明

项目提供两套配置文件：

### 1. **代码规范MCP配置.json**
- **用途**：专注于现有项目的架构分析和代码生成
- **适用场景**：为现有项目添加新功能、代码质量检查、架构分析
- **包含工具**：架构识别、代码生成、质量检查、测试生成

### 2. **完整开发流程MCP配置.json**  
- **用途**：覆盖从需求分析到代码实现的完整开发流程
- **适用场景**：新项目开发、需求文档解析、设计文档生成
- **包含工具**：需求解析、需求分析、架构设计、代码生成、测试

## 🚀 快速开始

### 步骤1：环境准备
1. **确保 Python 环境**
   ```bash
   python --version  # 确保 Python 3.7+
   ```

2. **检查工具文件**
   确保以下目录存在：
   ```
   d:\devolp\code1\easyCode\mcp-tools\
   ├── 01-requirements/
   ├── 02-design/
   ├── 03-architecture/
   ├── 04-generation/
   └── 05-testing/
   ```

### 步骤2：配置 Trae IDE
1. 打开 Trae IDE
2. 进入 **设置** → **MCP 配置**
3. 添加配置文件：
   - 基础功能：`d:\devolp\code1\easyCode\config\代码规范MCP配置.json`
   - 完整流程：`d:\devolp\code1\easyCode\config\完整开发流程MCP配置.json`
4. **重启 Trae IDE**

### 步骤3：验证配置
在 Trae IDE 中输入：
```
@project-architecture-analyzer 
```
如果出现工具提示，说明配置成功。

## 📖 使用场景详解

### 场景A：现有项目新功能开发 ⭐ 推荐

**适用情况**：为现有 Spring Boot/Node.js/Python 项目添加新功能

**使用步骤**：
```
1. 用户输入：
@project-architecture-analyzer 分析我的项目架构
项目路径：D:\your\project\path

2. AI 分析项目架构，识别：
- 架构模式（分层/微服务/六边形/DDD）
- 包结构和命名规范
- 技术栈和框架

3. 用户输入：
@intelligent-code-generator 基于现有架构生成订单管理模块
模块名：Order
字段：[
  {"name": "id", "type": "Long", "comment": "订单ID"},
  {"name": "customerId", "type": "Long", "comment": "客户ID"},
  {"name": "amount", "type": "BigDecimal", "comment": "订单金额"},
  {"name": "status", "type": "String", "comment": "订单状态"}
]

4. AI 生成完全匹配现有架构的代码：
- Controller（REST API）
- Service（业务逻辑）
- Repository（数据访问）
- Entity（实体类）
- DTO（数据传输对象）
```

### 场景B：代码质量检查

**使用步骤**：
```
@code-standard-checker 检查我的代码规范
项目路径：D:\your\project\path

AI 会检查：
✅ 命名规范（类名、方法名、变量名）
✅ 架构规则（分层架构、循环依赖）
✅ 安全规范（SQL注入、输入验证）
✅ 文档规范（JavaDoc、注释）
✅ 测试覆盖率
```

### 场景C：从需求到设计文档

**适用情况**：有产品需求，需要生成技术设计文档

**使用步骤**：
```
1. 需求解析：
@requirements-document-parser 解析需求
输入类型：codesign_url / screenshot_folder / document_file / direct_text
内容：[您的需求内容]

2. 需求分析：
@requirements-analyzer 分析产品需求
- 提取功能需求、非功能需求
- 识别用户角色和业务规则

3. 架构设计：
@architecture-designer 设计系统架构
- 推荐技术栈
- 设计系统架构图

4. 设计文档生成：
@design-document-generator 生成技术设计文档
- 输出完整的 Markdown 格式文档
- 包含架构、数据库、API 设计
```

### 场景D：设计文档到代码实现

**适用情况**：已有技术设计文档，直接生成代码

**使用步骤**：
```
1. 设计文档解析：
@design-document-parser 解析设计文档
文档路径：D:\your\design\document.md

2. 架构识别（如果是现有项目）：
@project-architecture-analyzer 分析现有项目架构

3. 代码生成：
@intelligent-code-generator 基于设计文档生成代码
- 严格按照设计文档实现
- 与现有项目架构保持一致
```

## 🛠️ 常用提示词模板

### 1. 项目架构分析
```
@project-architecture-analyzer 完整分析项目架构
项目路径：D:\your\project\path
分析深度：deep
置信度阈值：60

请识别：
- 架构模式类型
- 分层结构组织
- 命名约定规范
- 技术栈框架
- 代码模式特征
```

### 2. 智能代码生成
```
@intelligent-code-generator 生成[模块名]模块
模块名：User
功能描述：用户管理系统，包含注册、登录、个人信息管理
字段定义：[
  {"name": "id", "type": "Long", "comment": "用户ID", "nullable": false},
  {"name": "username", "type": "String", "comment": "用户名", "unique": true},
  {"name": "email", "type": "String", "comment": "邮箱", "unique": true},
  {"name": "password", "type": "String", "comment": "密码"},
  {"name": "createTime", "type": "LocalDateTime", "comment": "创建时间"}
]

请生成：
- 完整的 CRUD 操作
- 参数验证和异常处理
- 符合现有项目架构
```

### 3. 代码质量检查
```
@code-standard-checker 全面检查代码质量
项目路径：D:\your\project\path
检查范围：all
输出格式：json

检查项目：
- 命名规范合规性
- 架构规则遵循度
- 安全漏洞风险
- 文档完整性
- 测试覆盖率
```

### 4. 测试用例生成
```
@test-generator 生成完整测试用例
模块名：User
测试类型：[unit, integration, controller]
覆盖率要求：>85%
Mock框架：mockito

请生成：
- 单元测试（正常+异常场景）
- 集成测试（数据库交互）
- API测试（HTTP请求响应）
- 测试数据工厂
```

## ⚠️ 注意事项

### 1. 环境要求
- Python 3.7+ 环境
- Trae IDE 最新版本
- 项目文件读写权限

### 2. 路径配置
- 所有路径已配置为绝对路径
- 确保工具文件存在于指定位置
- Windows 路径使用双反斜杠 `\\`

### 3. 使用建议
- **首次使用**：建议在测试项目中验证
- **架构识别**：确保项目结构完整，代码示例充足
- **置信度检查**：验证架构识别的置信度是否足够（>60%）
- **持续优化**：根据使用反馈优化识别规则

### 4. 常见问题
- **工具无响应**：检查 Python 环境和文件路径
- **架构识别失败**：确保项目有足够的代码示例
- **生成代码不匹配**：重新运行架构分析，提高置信度

## 📊 效果预期

### 开发效率提升
- **架构识别**：自动化程度 95%
- **代码生成**：提升效率 80%
- **测试创建**：自动生成覆盖率 85%

### 代码质量保证
- **架构一致性**：100% 符合现有架构
- **编码规范**：100% 符合项目规范
- **文档完整性**：自动生成完整文档

## 🎯 最佳实践

1. **先分析，再生成**：始终先进行架构分析
2. **验证置信度**：确保架构识别置信度 >60%
3. **分步骤执行**：复杂功能分多个步骤实现
4. **及时测试**：生成代码后立即运行测试
5. **持续优化**：根据反馈调整配置参数

## 📝 实际使用示例

### 示例1：为 Spring Boot 项目添加商品管理功能

**场景**：现有电商项目，需要添加商品管理模块

```
步骤1：架构分析
用户：@project-architecture-analyzer 分析我的Spring Boot项目
项目路径：D:\ecommerce\backend

AI输出：
✅ 检测到分层架构（置信度：92%）
✅ 包结构：com.ecommerce.{controller,service,repository,entity}
✅ 命名约定：PascalCase类名，camelCase方法名
✅ 技术栈：Spring Boot 2.7, JPA, MySQL
✅ 代码模式：RESTful API, 统一异常处理, 参数验证

步骤2：生成商品模块
用户：@intelligent-code-generator 生成商品管理模块
模块名：Product
字段：[
  {"name": "id", "type": "Long", "comment": "商品ID"},
  {"name": "name", "type": "String", "comment": "商品名称"},
  {"name": "price", "type": "BigDecimal", "comment": "商品价格"},
  {"name": "categoryId", "type": "Long", "comment": "分类ID"},
  {"name": "stock", "type": "Integer", "comment": "库存数量"},
  {"name": "status", "type": "String", "comment": "商品状态"}
]

AI生成文件：
📁 src/main/java/com/ecommerce/
├── controller/ProductController.java
├── service/ProductService.java
├── repository/ProductRepository.java
├── entity/Product.java
└── dto/ProductCreateRequest.java, ProductUpdateRequest.java, ProductResponse.java

步骤3：质量检查
用户：@code-standard-checker 检查生成的代码质量

AI检查结果：
✅ 命名规范：100% 符合
✅ 架构规则：100% 符合
✅ 安全规范：通过
✅ 文档规范：JavaDoc 完整
```

### 示例2：从需求文档生成完整系统

**场景**：有产品需求文档，需要生成技术设计和代码

```
步骤1：需求解析
用户：我有一个用户管理系统的需求文档
@requirements-document-parser 解析需求
输入类型：document_file
内容：D:\requirements\user-management.md

步骤2：需求分析
@requirements-analyzer 分析产品需求

AI输出：
📋 功能需求：用户注册、登录、个人信息管理、角色权限
👥 用户角色：管理员、普通用户
🔒 非功能需求：安全性、性能、可扩展性
📏 业务规则：密码复杂度、会话超时、权限控制

步骤3：架构设计
@architecture-designer 设计系统架构

AI推荐：
🏗️ 架构模式：分层架构
💻 技术栈：Spring Boot + Spring Security + JWT + MySQL
🔧 部署方案：Docker + Nginx

步骤4：生成设计文档
@design-document-generator 生成技术设计文档

AI输出：完整的 Markdown 技术设计文档，包含：
- 系统架构图
- 数据库设计
- API 接口定义
- 安全方案
- 部署架构
```

## 🔧 故障排除

### 常见问题及解决方案

#### 1. MCP 工具无法启动
**症状**：在 Trae IDE 中调用工具时无响应

**解决方案**：
```bash
# 检查 Python 环境
python --version

# 检查文件是否存在
dir "d:\devolp\code1\easyCode\mcp-tools\03-architecture\项目架构识别MCP工具.py"

# 检查配置文件路径
# 确保 Trae IDE 中的配置路径正确
```

#### 2. 架构识别置信度低
**症状**：架构识别置信度 <50%

**解决方案**：
- 确保项目有足够的代码文件（>10个类）
- 检查项目结构是否规范
- 增加代码示例的多样性
- 调整置信度阈值：`"CONFIDENCE_THRESHOLD": "40"`

#### 3. 生成的代码不符合项目规范
**症状**：生成的代码风格与现有代码不一致

**解决方案**：
```
1. 重新运行架构分析：
@project-architecture-analyzer 深度分析项目架构
分析深度：deep
包含更多代码示例

2. 检查分析结果：
验证命名约定、包结构、代码模式是否正确识别

3. 手动指定规范：
在生成代码时明确指定：
- 包名规范
- 命名约定
- 代码模式
```

#### 4. 工具执行超时
**症状**：大型项目分析时工具执行超时

**解决方案**：
- 调整环境变量：`"ANALYSIS_DEPTH": "shallow"`
- 排除不必要的目录：`"EXCLUDE_PATTERNS": "node_modules,target,build,dist,.git,test"`
- 分模块分析，避免一次性分析整个项目

### 性能优化建议

#### 1. 大型项目优化
```json
{
  "env": {
    "ANALYSIS_DEPTH": "shallow",
    "EXCLUDE_PATTERNS": "node_modules,target,build,dist,.git,test,docs",
    "INCLUDE_EXTENSIONS": ".java,.js,.ts,.py",
    "MAX_FILES": "100"
  }
}
```

#### 2. 提高识别准确性
```json
{
  "env": {
    "CONFIDENCE_THRESHOLD": "70",
    "ANALYSIS_DEPTH": "deep",
    "SAMPLE_SIZE": "50"
  }
}
```

## 📚 进阶使用技巧

### 1. 自定义架构模式
如果您的项目使用特殊架构，可以：
- 在 `项目架构识别MCP工具.py` 中添加自定义识别逻辑
- 在 `智能代码生成MCP工具.py` 中添加对应的生成模板
- 创建自定义模板文件

### 2. 批量代码生成
```
@intelligent-code-generator 批量生成多个模块
模块列表：[
  {"name": "User", "fields": [...]},
  {"name": "Product", "fields": [...]},
  {"name": "Order", "fields": [...]}
]
```

### 3. 增量开发
```
# 第一次：生成基础模块
@intelligent-code-generator 生成User基础模块

# 第二次：添加新功能
@intelligent-code-generator 为User模块添加权限管理功能
基于现有代码：src/main/java/com/example/user/
```

## 🎯 团队协作建议

### 1. 统一配置
- 团队共享同一套 MCP 配置文件
- 统一项目架构识别规则
- 建立代码生成规范

### 2. 代码审查
- 生成代码后进行人工审查
- 验证业务逻辑正确性
- 确保安全性和性能

### 3. 持续改进
- 收集团队使用反馈
- 优化识别规则和生成模板
- 定期更新工具配置

---

**这套智能架构识别的完整开发流程 MCP 工具链，让您的代码生成不再是固定模板的简单套用，而是真正理解项目架构的智能创造！**
