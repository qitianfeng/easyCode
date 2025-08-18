# OceanBase MCP 配置完整教程

## 目录
1. [MCP 简介](#mcp-简介)
2. [环境准备](#环境准备)
3. [OceanBase MCP Server 安装](#oceanbase-mcp-server-安装)
4. [Trae IDE 集成配置](#trae-ide-集成配置)
5. [MySQL 租户配置](#mysql-租户配置)
6. [Oracle 租户配置](#oracle-租户配置)
7. [多租户同时配置](#多租户同时配置)
8. [功能测试](#功能测试)
9. [常见问题](#常见问题)
10. [高级配置](#高级配置)

## MCP 简介

MCP（Model Context Protocol）是 Anthropic 公司于 2024 年 11 月推出的模型上下文协议，被称为"大模型时代的 USB 接口"。它允许 AI 模型与各种数据源和工具进行标准化连接。

### 主要特性
- 标准化的协议接口
- 支持多种数据源连接
- 实时数据交互
- 安全的访问控制

## 环境准备

### 系统要求
- **操作系统**：Windows 10+、macOS 10.15+、Ubuntu 18.04+
- **Node.js**：16.0+ 或 Python 3.8+
- **内存**：至少 4GB RAM
- **网络**：能够访问 OceanBase 集群

### 必需软件
```bash
# 检查 Node.js 版本
node --version

# 检查 Python 版本
python --version

# 安装 Git
git --version
```

## OceanBase MCP Server 安装

### 1. 克隆项目
```bash
# 克隆官方仓库
git clone https://github.com/oceanbase/mcp-server-oceanbase.git
cd mcp-server-oceanbase
```

### 2. 安装依赖
```bash
# 使用 npm（推荐）
npm install

# 或使用 yarn
yarn install

# Python 版本（如果适用）
pip install -r requirements.txt
```

### 3. 构建项目
```bash
# 构建 TypeScript 项目
npm run build

# 或直接运行开发模式
npm run dev
```

## Trae IDE 集成配置

### 1. 下载安装 Trae IDE
1. 访问 [Trae 官网](https://trae.ai/)
2. 下载适合您操作系统的版本
3. 按照安装向导完成安装

### 2. 打开 MCP 配置
1. 启动 Trae IDE
2. 点击右上角设置图标 ⚙️
3. 选择 "MCP Servers" 或 "扩展设置"
4. 点击 "添加新的 MCP Server"

## MySQL 租户配置

### 基础配置文件
创建 `mysql-config.json`：
```json
{
  "oceanbase_mysql": {
    "host": "127.0.0.1",
    "port": 2881,
    "user": "root@mysql_tenant",
    "password": "your_mysql_password",
    "database": "test",
    "charset": "utf8mb4",
    "dialect": "mysql",
    "options": {
      "connectTimeout": 60000,
      "acquireTimeout": 60000,
      "timeout": 60000,
      "pool": {
        "max": 10,
        "min": 0,
        "idle": 10000
      }
    }
  },
  "server": {
    "name": "oceanbase-mysql-mcp",
    "version": "1.0.0",
    "description": "OceanBase MySQL 租户 MCP Server"
  }
}
```

### Trae IDE MCP 配置
在 Trae IDE 的 MCP 配置中添加：
```json
{
  "mcpServers": {
    "oceanbase-mysql": {
      "command": "node",
      "args": [
        "/path/to/mcp-server-oceanbase/dist/index.js"
      ],
      "env": {
        "OCEANBASE_HOST": "127.0.0.1",
        "OCEANBASE_PORT": "2881",
        "OCEANBASE_USER": "root@mysql_tenant",
        "OCEANBASE_PASSWORD": "your_mysql_password",
        "OCEANBASE_DATABASE": "test",
        "OCEANBASE_DIALECT": "mysql",
        "MCP_SERVER_NAME": "OceanBase-MySQL"
      }
    }
  }
}
```

### MySQL 租户连接字符串格式
```
mysql://username@tenant_name:password@host:port/database
```

示例：
```
mysql://root@mysql_tenant:password@127.0.0.1:2881/test
```

## Oracle 租户配置

### 基础配置文件
创建 `oracle-config.json`：
```json
{
  "oceanbase_oracle": {
    "host": "127.0.0.1",
    "port": 2881,
    "user": "SYS@oracle_tenant",
    "password": "your_oracle_password",
    "database": "ORCL",
    "dialect": "oracle",
    "options": {
      "connectTimeout": 60000,
      "acquireTimeout": 60000,
      "timeout": 60000,
      "pool": {
        "max": 10,
        "min": 0,
        "idle": 10000
      }
    }
  },
  "server": {
    "name": "oceanbase-oracle-mcp",
    "version": "1.0.0",
    "description": "OceanBase Oracle 租户 MCP Server"
  }
}
```

### Trae IDE MCP 配置
```json
{
  "mcpServers": {
    "oceanbase-oracle": {
      "command": "node",
      "args": [
        "/path/to/mcp-server-oceanbase/dist/index.js"
      ],
      "env": {
        "OCEANBASE_HOST": "127.0.0.1",
        "OCEANBASE_PORT": "2881",
        "OCEANBASE_USER": "SYS@oracle_tenant",
        "OCEANBASE_PASSWORD": "your_oracle_password",
        "OCEANBASE_DATABASE": "ORCL",
        "OCEANBASE_DIALECT": "oracle",
        "MCP_SERVER_NAME": "OceanBase-Oracle"
      }
    }
  }
}
```

### Oracle 租户连接字符串格式
```
oracle://username@tenant_name:password@host:port/database
```

示例：
```
oracle://SYS@oracle_tenant:password@127.0.0.1:2881/ORCL
```

## 多租户同时配置

### 完整的多租户配置
```json
{
  "mcpServers": {
    "oceanbase-mysql-tenant": {
      "command": "node",
      "args": ["/path/to/mcp-server-oceanbase/dist/index.js"],
      "env": {
        "OCEANBASE_HOST": "127.0.0.1",
        "OCEANBASE_PORT": "2881",
        "OCEANBASE_USER": "root@mysql_tenant",
        "OCEANBASE_PASSWORD": "mysql_password",
        "OCEANBASE_DATABASE": "test",
        "OCEANBASE_DIALECT": "mysql",
        "MCP_SERVER_NAME": "OceanBase-MySQL-租户"
      }
    },
    "oceanbase-oracle-tenant": {
      "command": "node",
      "args": ["/path/to/mcp-server-oceanbase/dist/index.js"],
      "env": {
        "OCEANBASE_HOST": "127.0.0.1",
        "OCEANBASE_PORT": "2881",
        "OCEANBASE_USER": "SYS@oracle_tenant",
        "OCEANBASE_PASSWORD": "oracle_password",
        "OCEANBASE_DATABASE": "ORCL",
        "OCEANBASE_DIALECT": "oracle",
        "MCP_SERVER_NAME": "OceanBase-Oracle-租户"
      }
    }
  }
}
```

### 租户切换使用
在 Trae IDE 中，您可以通过以下方式指定使用哪个租户：
```
@OceanBase-MySQL-租户 查询用户表结构
@OceanBase-Oracle-租户 查询系统视图
```

## 功能测试

### MySQL 租户测试命令
```sql
-- 基础连接测试
SELECT @@version_comment;
SELECT @@version;

-- 数据库列表
SHOW DATABASES;

-- 表列表
SHOW TABLES;

-- 表结构查询
DESCRIBE table_name;
SHOW CREATE TABLE table_name;

-- 数据查询
SELECT * FROM table_name LIMIT 10;
```

### Oracle 租户测试命令
```sql
-- 基础连接测试
SELECT * FROM V$VERSION;
SELECT USER FROM DUAL;

-- 用户列表
SELECT USERNAME FROM ALL_USERS;

-- 表列表
SELECT TABLE_NAME FROM USER_TABLES;

-- 表结构查询
SELECT COLUMN_NAME, DATA_TYPE, DATA_LENGTH
FROM USER_TAB_COLUMNS
WHERE TABLE_NAME = 'TABLE_NAME';

-- 数据查询
SELECT * FROM table_name WHERE ROWNUM <= 10;
```

### 在 Trae IDE 中的自然语言测试
```
用户：帮我查看数据库中有哪些表
用户：描述一下 users 表的结构
用户：查询 orders 表中最近10条记录
用户：帮我写一个统计用户数量的 SQL
用户：分析一下销售数据的趋势
```

## 常见问题

### 1. 连接失败问题
**问题**：无法连接到 OceanBase 数据库
**解决方案**：
```bash
# 检查网络连通性
ping your-oceanbase-host

# 检查端口是否开放
telnet your-oceanbase-host 2881

# 验证用户名密码
mysql -h your-oceanbase-host -P 2881 -u root@tenant_name -p
```

### 2. 权限错误
**问题**：用户权限不足
**解决方案**：
```sql
-- 检查用户权限
SHOW GRANTS FOR 'username'@'tenant_name';

-- 授予必要权限（需要管理员执行）
GRANT SELECT, INSERT, UPDATE, DELETE ON database.* TO 'username'@'tenant_name';
```

### 3. MCP Server 启动失败
**问题**：MCP Server 无法启动
**解决方案**：
```bash
# 检查依赖
npm list

# 重新安装依赖
rm -rf node_modules package-lock.json
npm install

# 检查配置文件
node -c config.json

# 查看详细错误日志
npm run dev -- --verbose
```

### 4. Trae IDE 无法识别 MCP Server
**问题**：Trae IDE 中看不到 MCP Server
**解决方案**：
1. 检查配置文件路径是否正确
2. 重启 Trae IDE
3. 查看 Trae IDE 日志：帮助 → 开发者工具 → 控制台
4. 确认 MCP Server 进程正在运行

## 高级配置

### 1. 安全配置
```json
{
  "security": {
    "allowedOperations": ["SELECT", "SHOW", "DESCRIBE", "EXPLAIN"],
    "blockedTables": ["sensitive_data", "user_passwords"],
    "blockedSchemas": ["information_schema", "performance_schema"],
    "queryTimeout": 30000,
    "maxRows": 1000,
    "enableAuditLog": true
  }
}
```

### 2. 性能优化配置
```json
{
  "performance": {
    "connectionPool": {
      "max": 20,
      "min": 5,
      "idle": 10000,
      "acquire": 30000,
      "evict": 1000
    },
    "queryCache": {
      "enabled": true,
      "maxSize": 100,
      "ttl": 300000
    },
    "compression": true
  }
}
```

### 3. 日志配置
```json
{
  "logging": {
    "level": "info",
    "file": "./logs/mcp-server.log",
    "maxSize": "10m",
    "maxFiles": 5,
    "format": "json"
  }
}
```

### 4. 自定义工具配置
```json
{
  "tools": [
    {
      "name": "query_database",
      "description": "执行数据库查询",
      "parameters": {
        "sql": {
          "type": "string",
          "description": "要执行的 SQL 语句"
        },
        "limit": {
          "type": "number",
          "description": "返回结果的最大行数",
          "default": 100
        }
      }
    },
    {
      "name": "analyze_performance",
      "description": "分析查询性能",
      "parameters": {
        "query": {
          "type": "string",
          "description": "要分析的查询语句"
        }
      }
    },
    {
      "name": "get_table_info",
      "description": "获取表结构信息",
      "parameters": {
        "table_name": {
          "type": "string",
          "description": "表名"
        },
        "include_indexes": {
          "type": "boolean",
          "description": "是否包含索引信息",
          "default": false
        }
      }
    }
  ]
}
```

## 使用示例

### 1. 数据查询示例
```
用户：帮我查询订单表中今天的订单数量
AI：我来为您查询今天的订单数量...

执行的 SQL：
SELECT COUNT(*) as order_count
FROM orders
WHERE DATE(created_at) = CURDATE();

结果：今天共有 156 个订单
```

### 2. 表结构分析示例
```
用户：分析一下用户表的结构，看看有什么优化建议
AI：我来分析用户表的结构...

表结构分析：
- 表名：users
- 字段数：8
- 主键：id (AUTO_INCREMENT)
- 索引：email (UNIQUE), created_at
- 建议：可以为 status 字段添加索引以提高查询性能
```

### 3. 性能优化示例
```
用户：这个查询很慢，帮我优化：SELECT * FROM orders WHERE customer_id = 123 AND status = 'pending'
AI：我来分析这个查询的性能...

优化建议：
1. 添加复合索引：CREATE INDEX idx_customer_status ON orders(customer_id, status);
2. 避免使用 SELECT *，只选择需要的字段
3. 优化后的查询：SELECT id, order_date, amount FROM orders WHERE customer_id = 123 AND status = 'pending';
```

## 总结

通过本教程，您已经学会了：
1. 安装和配置 OceanBase MCP Server
2. 在 Trae IDE 中集成 MCP Server
3. 配置 MySQL 和 Oracle 两种租户类型
4. 进行功能测试和问题排查
5. 使用高级配置优化性能和安全性

现在您可以在 Trae IDE 中通过自然语言与 OceanBase 数据库进行交互，大大提高数据库操作的效率！

## 参考资源

- [OceanBase 官方文档](https://www.oceanbase.com/docs/)
- [MCP 协议规范](https://modelcontextprotocol.io/)
- [Trae IDE 官网](https://trae.ai/)
- [OceanBase MCP Server GitHub](https://github.com/oceanbase/mcp-server-oceanbase)
