# Claude Desktop MCP 配置指南

## 配置文件状态
✅ **可以直接使用** - `config/完整MCP配置.json` 已经过测试验证，所有 MCP 服务器都能正常工作。

## 使用步骤

### 1. 找到 Claude Desktop 配置文件
Claude Desktop 的配置文件位置：
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### 2. 备份现有配置
在修改前，请先备份您现有的配置文件。

### 3. 添加 MCP 配置
将 `config/完整MCP配置.json` 的内容添加到您的 Claude Desktop 配置文件中。

**示例完整配置**：
```json
{
  "mcpServers": {
    "requirements-analyzer": {
      "command": "python",
      "args": [
        "d:\\devolp\\code1\\easyCode\\mcp-tools\\01-requirements\\标准需求分析MCP服务器.py"
      ],
      "description": "需求分析工具 - 分析产品需求，生成技术规格"
    },
    "design-generator": {
      "command": "python",
      "args": [
        "d:\\devolp\\code1\\easyCode\\mcp-tools\\02-design\\标准设计文档MCP服务器.py"
      ],
      "description": "设计文档生成工具 - 生成设计文档和API设计"
    },
    "architecture-analyzer": {
      "command": "python",
      "args": [
        "d:\\devolp\\code1\\easyCode\\mcp-tools\\03-architecture\\标准架构分析MCP服务器.py"
      ],
      "description": "架构分析工具 - 分析项目架构模式"
    },
    "code-generator": {
      "command": "python",
      "args": [
        "d:\\devolp\\code1\\easyCode\\mcp-tools\\04-generation\\标准代码生成MCP服务器.py"
      ],
      "description": "代码生成工具 - 生成完整的CRUD模块"
    },
    "test-generator": {
      "command": "python",
      "args": [
        "d:\\devolp\\code1\\easyCode\\mcp-tools\\05-testing\\标准测试生成MCP服务器.py"
      ],
      "description": "测试生成工具 - 生成单元测试和集成测试"
    },
    "documentation-generator": {
      "command": "python",
      "args": [
        "d:\\devolp\\code1\\easyCode\\mcp-tools\\05-testing\\标准文档生成MCP服务器.py"
      ],
      "description": "文档生成工具 - 生成API文档和README"
    }
  }
}
```

### 4. 重要注意事项

#### 路径配置
- ⚠️ **必须修改路径**：配置中的路径 `d:\\devolp\\code1\\easyCode\\` 是我的测试环境路径
- ✅ **请替换为您的实际路径**：将所有路径中的 `d:\\devolp\\code1\\easyCode\\` 替换为您项目的实际路径

#### Python 环境
- ✅ **Python 可用**：确保系统 PATH 中有 `python` 命令
- ✅ **版本要求**：Python 3.7+ （推荐 3.8+）
- ✅ **依赖安装**：所有工具都使用标准库，无需额外安装依赖

#### 文件权限
- ✅ **执行权限**：确保 Python 文件有执行权限
- ✅ **路径访问**：确保 Claude Desktop 能访问指定路径

### 5. 验证配置

#### 重启 Claude Desktop
配置修改后，需要重启 Claude Desktop 应用。

#### 检查工具是否加载
重启后，在 Claude Desktop 中应该能看到新的 MCP 工具。您可以询问：
- "你现在有哪些 MCP 工具可用？"
- "帮我分析一下需求"
- "生成一个用户实体的代码"

#### 测试工具功能
可以尝试使用各个工具：
```
请使用需求分析工具分析以下需求：
开发一个在线书店系统，支持图书浏览、购买、用户管理功能
```

### 6. 故障排除

#### 常见问题
1. **工具不显示**：检查路径是否正确，Python 是否可用
2. **权限错误**：确保文件有执行权限
3. **路径错误**：使用绝对路径，注意 Windows 路径中的反斜杠转义

#### 调试方法
1. 在命令行中直接运行 Python 文件测试
2. 检查 Claude Desktop 的日志文件
3. 使用我们提供的测试脚本验证工具状态

### 7. 可用的 MCP 工具

配置成功后，您将拥有以下工具：

| 工具名称 | 功能描述 | 主要用途 |
|---------|---------|---------|
| requirements-analyzer | 需求分析工具 | 分析产品需求，生成技术规格 |
| design-generator | 设计文档生成工具 | 生成设计文档和API设计 |
| architecture-analyzer | 架构分析工具 | 分析项目架构模式 |
| code-generator | 代码生成工具 | 生成完整的CRUD模块 |
| test-generator | 测试生成工具 | 生成单元测试和集成测试 |
| documentation-generator | 文档生成工具 | 生成API文档和README |

## 总结
✅ 配置文件已验证可用  
⚠️ 需要修改路径为您的实际项目路径  
🎉 配置成功后即可享受完整的开发工具链支持！
