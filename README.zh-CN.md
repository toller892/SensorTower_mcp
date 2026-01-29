# Sensor Tower MCP Server（双 Token 版本）

一个基于 FastMCP 的 MCP 服务器，让 AI 助手能够使用 Sensor Tower API 获取应用市场数据，支持双 Token 自动切换。

## ✨ 新功能：双 Token 自动切换

当主 API Token 配额用完时，服务器会自动切换到备用 Token，确保服务不中断！

### 工作原理

```
主 Token 正常工作 → 配额耗尽 (429/403) → 自动切换到备用 Token → 继续服务
```

### 配置示例

```bash
# .env 文件
SENSOR_TOWER_API_TOKEN=st_primary_token_xxx
SENSOR_TOWER_API_TOKEN_BACKUP=st_backup_token_yyy
```

## 📋 功能特性

- ✅ 40+ 个 Sensor Tower API 工具
- ✅ 双 Token 自动故障转移
- ✅ 支持 stdio 和 HTTP 传输模式
- ✅ 完整的文档和示例
- ✅ Docker 支持
- ✅ 自动重试和错误处理

## 🚀 快速开始

### 1. 安装依赖

```bash
# 使用 uv（推荐）
uv sync

# 或使用 pip
pip install -e .[test]
```

### 2. 配置 API Token

复制 `.env.example` 为 `.env` 并填入你的 Token：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```bash
# 主 Token（必需）
SENSOR_TOWER_API_TOKEN=st_your_primary_token

# 备用 Token（推荐）
SENSOR_TOWER_API_TOKEN_BACKUP=st_your_backup_token
```

### 3. 启动服务器

#### Windows 用户

双击运行 `start_server.bat` 或在命令行执行：

```cmd
start_server.bat
```

#### 命令行启动

```bash
# 使用 Python 3.13
py -3.13 -m sensortower_mcp.server

# 或使用默认 Python
python -m sensortower_mcp.server
```

### 4. 配置 MCP 客户端

#### Cursor IDE

在 Cursor 设置中添加 MCP 服务器：

```json
{
  "mcpServers": {
    "sensortower": {
      "command": "python",
      "args": ["-m", "sensortower_mcp.server"],
      "env": {
        "SENSOR_TOWER_API_TOKEN": "st_primary_token",
        "SENSOR_TOWER_API_TOKEN_BACKUP": "st_backup_token"
      }
    }
  }
}
```

#### Claude Desktop

在 Claude Desktop 配置文件中添加：

```json
{
  "mcpServers": {
    "sensortower": {
      "command": "python",
      "args": ["-m", "sensortower_mcp.server"],
      "env": {
        "SENSOR_TOWER_API_TOKEN": "st_primary_token",
        "SENSOR_TOWER_API_TOKEN_BACKUP": "st_backup_token"
      }
    }
  }
}
```

更多配置示例请查看 `mcp-config-examples.json`。

## 📊 可用工具分类

### 应用分析 (16 个工具)
- `get_app_metadata` - 获取应用详细信息
- `get_download_estimates` - 下载量估算
- `get_revenue_estimates` - 收入估算
- `get_creatives` - 广告创意数据
- `top_in_app_purchases` - 热门内购项目
- 等等...

### 市场分析 (12 个工具)
- `get_category_rankings` - 分类排行榜
- `get_top_and_trending` - 热门和趋势应用
- `search_entities` - 搜索应用和发行商
- `usage_top_apps` - 活跃用户排行
- 等等...

### 商店营销 (6 个工具)
- `get_featured_apps` - 精选应用
- `get_keywords` - 关键词排名
- `get_reviews` - 应用评论
- 等等...

### 你的应用数据 (5 个工具)
- `analytics_metrics` - 分析指标
- `sales_reports` - 销售报告
- 等等...

### 实用工具 (4 个工具)
- `get_country_codes` - 国家代码
- `get_category_ids` - 分类 ID
- `health_check` - 健康检查

## 🔄 双 Token 切换演示

启动时显示：
```
🚀 Starting Sensor Tower MCP Server (FastMCP)
📡 API Base URL: https://api.sensortower.com
🚌 Transport: stdio
🔧 Available tools: 40
🔑 API Tokens configured: 2 (Primary + Backup)
```

当主 Token 配额用完时：
```
⚠️  Switching to backup token #2
🔄 Retrying request with backup token...
```

## 🧪 测试

运行 Token 切换测试：

```bash
py -3.13 test_dual_token.py
```

预期输出：
```
🧪 Testing Token Failover Mechanism

✓ Initial token: st_primary_token_123
✓ Switching to backup token...
⚠️  Switching to backup token #2
✓ Now using: st_backup_token_456
...
✅ All token failover tests passed!
```

## 📖 文档

- [双 Token 配置指南](DUAL_TOKEN_GUIDE.md) - 详细的配置和使用说明
- [MCP 配置示例](mcp-config-examples.json) - 各种客户端的配置示例
- [英文 README](README.md) - 原始英文文档

## 🐳 Docker 部署

```bash
# 构建镜像
docker build -t sensortower-mcp .

# 运行容器（双 Token）
docker run --rm \
  -e SENSOR_TOWER_API_TOKEN=st_primary_token \
  -e SENSOR_TOWER_API_TOKEN_BACKUP=st_backup_token \
  -p 8666:8666 \
  sensortower-mcp

# 使用 Docker Compose
docker compose up -d
```

## 🔑 获取 API Token

访问 Sensor Tower 控制台获取 API Token：
https://app.sensortower.com/users/edit/api-settings

建议：
- 为主 Token 和备用 Token 使用不同的配额计划
- 定期监控配额使用情况
- 设置配额告警通知

## ⚠️ 注意事项

1. **Token 安全**
   - 不要将 Token 提交到版本控制系统
   - 使用 `.env` 文件并确保它在 `.gitignore` 中
   - 定期轮换 API Token

2. **配额管理**
   - 监控两个 Token 的配额使用情况
   - 避免两个 Token 同时耗尽
   - 考虑使用不同的配额计划

3. **Token 切换**
   - 切换后不会自动切回主 Token
   - 需要重启服务器才能重置到主 Token
   - 切换会在日志中记录

## 🛠️ 故障排除

### 问题：备用 Token 没有生效

检查：
- 环境变量名称是否正确：`SENSOR_TOWER_API_TOKEN_BACKUP`
- Token 格式是否正确（以 `st_` 开头）
- 启动日志是否显示 "API Tokens configured: 2"

### 问题：切换后仍然报错

可能原因：
- 备用 Token 也已达到配额限制
- 备用 Token 无效或已过期
- 其他类型的 API 错误

解决方法：
- 在 Sensor Tower 控制台检查 Token 状态
- 查看详细错误日志
- 验证两个 Token 都有效

## 📝 更新日志

### v1.2.10+ (双 Token 版本)
- ✨ 新增：双 API Token 支持
- ✨ 新增：自动故障转移机制
- ✨ 新增：配额错误检测（429, 403）
- 📚 新增：中文文档和配置示例
- 🧪 新增：Token 切换测试脚本
- 🚀 新增：Windows 启动脚本

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

请参考原项目许可证。

## 🔗 相关链接

- 原始项目：https://github.com/virusimmortal00/sensortower-mcp
- 本项目：https://github.com/toller892/SensorTower_mcp
- Sensor Tower API：https://app.sensortower.com/api/docs
- FastMCP 文档：https://github.com/jlowin/fastmcp
