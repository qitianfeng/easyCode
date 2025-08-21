# EasyCode - MCP 开发工具链

一个完整的 MCP (Model Context Protocol) 开发工具链，为 Claude Desktop 提供强大的软件开发支持。

## 🚀 快速开始

### 1. 配置 Claude Desktop
```bash
# 生成适合您环境的配置
python generate_mcp_config.py
```

### 2. 复制配置到 Claude Desktop
将生成的 `claude_desktop_mcp_config.json` 内容添加到您的 Claude Desktop 配置文件中。

### 3. 重启 Claude Desktop
重启应用以加载新的 MCP 工具。

## 🛠️ 可用工具

| 工具 | 功能 | 文件 |
|------|------|------|
| 需求分析 | 分析产品需求，生成技术规格 | `01-requirements/标准需求分析MCP服务器.py` |
| 设计文档 | 生成设计文档和API设计 | `02-design/标准设计文档MCP服务器.py` |
| 架构分析 | 分析项目架构模式 | `03-architecture/标准架构分析MCP服务器.py` |
| 代码生成 | 生成完整的CRUD模块 | `04-generation/标准代码生成MCP服务器.py` |
| 测试生成 | 生成单元测试和集成测试 | `05-testing/标准测试生成MCP服务器.py` |
| 文档生成 | 生成API文档和README | `05-testing/标准文档生成MCP服务器.py` |
| 简化版 | 整合多个工具的简化服务器 | `simple-mcp-server.py` |

## 📚 文档

- [配置指南](docs/Claude_Desktop_MCP配置指南.md) - 详细的配置步骤
- [测试报告](docs/MCP工具测试报告.md) - 功能测试结果
- [工具说明](docs/simple-mcp-server说明.md) - 各工具的详细说明
- [使用指南](docs/MCP工具链使用指南.md) - 完整使用指南

## 🏗️ 项目结构

```
easyCode/
├── README.md                           # 项目说明
├── claude_desktop_mcp_config.json      # MCP 配置文件
├── generate_mcp_config.py              # 配置生成工具
├── docs/                              # 文档目录
├── mcp-tools/                         # MCP 工具
│   ├── simple-mcp-server.py           # 简化版服务器
│   ├── 01-requirements/               # 需求分析工具
│   ├── 02-design/                     # 设计文档工具
│   ├── 03-architecture/               # 架构分析工具
│   ├── 04-generation/                 # 代码生成工具
│   └── 05-testing/                    # 测试和文档生成工具
└── archive/                           # 归档文件
```

## ⚡ 使用示例

在 Claude Desktop 中，您可以这样使用：

```
请使用需求分析工具分析以下需求：
开发一个在线书店系统，支持图书浏览、购买、用户管理功能
```

```
请使用代码生成工具为 Book 实体生成 CRUD 代码，包含以下字段：
- title (String)
- author (String) 
- price (BigDecimal)
- isbn (String)
```

## 🔧 开发

### 环境要求
- Python 3.7+
- Claude Desktop

### 测试工具
所有 MCP 工具都经过完整测试，确保功能正常。

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！
