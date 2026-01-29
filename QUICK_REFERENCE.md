# 🚀 Sensor Tower MCP 双 Token 快速参考

## ⚡ 5 分钟快速开始

### 1️⃣ 配置 Token
```bash
# 复制配置文件
cp .env.example .env

# 编辑 .env 文件
SENSOR_TOWER_API_TOKEN=st_your_primary_token
SENSOR_TOWER_API_TOKEN_BACKUP=st_your_backup_token
```

### 2️⃣ 启动服务器
```bash
# Windows
start_server.bat

# 或命令行
py -3.13 -m sensortower_mcp.server
```

### 3️⃣ 配置 MCP 客户端
```json
{
  "mcpServers": {
    "sensortower": {
      "command": "python",
      "args": ["-m", "sensortower_mcp.server"],
      "env": {
        "SENSOR_TOWER_API_TOKEN": "st_primary",
        "SENSOR_TOWER_API_TOKEN_BACKUP": "st_backup"
      }
    }
  }
}
```

---

## 📋 常用命令

| 操作 | 命令 |
|------|------|
| 启动服务器 | `py -3.13 -m sensortower_mcp.server` |
| HTTP 模式 | `py -3.13 -m sensortower_mcp.server --transport http --port 8666` |
| 测试 Token 切换 | `py -3.13 test_dual_token.py` |
| 查看日志 | 启动时自动显示 |
| 健康检查 | `curl http://localhost:8666/health` (HTTP 模式) |

---

## 🔑 环境变量

| 变量名 | 必需 | 说明 |
|--------|------|------|
| `SENSOR_TOWER_API_TOKEN` | ✅ | 主 API Token |
| `SENSOR_TOWER_API_TOKEN_BACKUP` | ⭕ | 备用 API Token（推荐） |
| `API_BASE_URL` | ❌ | API 基础 URL（默认：https://api.sensortower.com） |
| `TRANSPORT` | ❌ | 传输模式（默认：stdio） |
| `PORT` | ❌ | HTTP 端口（默认：8666） |

---

## 🎯 Token 切换触发条件

| HTTP 状态码 | 条件 | 行为 |
|------------|------|------|
| 429 | Too Many Requests | ✅ 自动切换 |
| 403 | Forbidden + 配额关键词 | ✅ 自动切换 |
| 500, 502, 503, 504 | 服务器错误 | ⏱️ 重试（不切换） |
| 其他 | - | ❌ 抛出错误 |

**配额关键词：** `quota`, `limit`, `exceeded`, `rate`

---

## 📊 启动信息解读

```
🚀 Starting Sensor Tower MCP Server (FastMCP)
📡 API Base URL: https://api.sensortower.com
🚌 Transport: stdio
🔧 Available tools: 40
🔑 API Tokens configured: 2 (Primary + Backup)  ← 这里显示 Token 数量
```

---

## 🔄 Token 切换日志

```
⚠️  Switching to backup token #2  ← Token 切换通知
🔄 Retrying request with backup token...  ← 重试请求
```

---

## 🛠️ 常见问题速查

### ❓ 备用 Token 没有生效？

**检查清单：**
- [ ] 环境变量名称正确：`SENSOR_TOWER_API_TOKEN_BACKUP`
- [ ] Token 格式正确（以 `st_` 开头）
- [ ] 启动日志显示 "API Tokens configured: 2"
- [ ] .env 文件在正确位置

### ❓ 切换后仍然报错？

**可能原因：**
1. 备用 Token 也达到配额限制
2. 备用 Token 无效或过期
3. 其他类型的 API 错误（非配额）

**解决方法：**
1. 在 Sensor Tower 控制台检查 Token 状态
2. 查看详细错误日志
3. 验证两个 Token 都有效

### ❓ 如何重置到主 Token？

**方法：** 重启服务器

```bash
# 停止服务器（Ctrl+C）
# 重新启动
py -3.13 -m sensortower_mcp.server
```

---

## 📁 重要文件位置

| 文件 | 用途 |
|------|------|
| `.env` | 环境变量配置（需自己创建） |
| `.env.example` | 配置模板 |
| `.env.local.example` | 详细配置示例 |
| `start_server.bat` | Windows 启动脚本 |
| `test_dual_token.py` | Token 切换测试 |
| `README.zh-CN.md` | 中文完整文档 |
| `DUAL_TOKEN_GUIDE.md` | 双 Token 详细指南 |
| `mcp-config-examples.json` | MCP 客户端配置示例 |

---

## 🔗 获取 API Token

**Sensor Tower 控制台：**  
https://app.sensortower.com/users/edit/api-settings

**建议：**
- 为主 Token 和备用 Token 设置不同名称
- 使用不同的配额计划
- 定期检查配额使用情况

---

## 🎨 MCP 客户端配置速查

### Cursor
```json
{
  "mcpServers": {
    "sensortower": {
      "command": "python",
      "args": ["-m", "sensortower_mcp.server"],
      "env": {
        "SENSOR_TOWER_API_TOKEN": "st_xxx",
        "SENSOR_TOWER_API_TOKEN_BACKUP": "st_yyy"
      }
    }
  }
}
```

### Claude Desktop
同上配置

### Kiro
同上配置

### Windows (py launcher)
```json
{
  "mcpServers": {
    "sensortower": {
      "command": "py",
      "args": ["-3.13", "-m", "sensortower_mcp.server"],
      "env": {
        "SENSOR_TOWER_API_TOKEN": "st_xxx",
        "SENSOR_TOWER_API_TOKEN_BACKUP": "st_yyy"
      }
    }
  }
}
```

---

## 🐳 Docker 快速命令

```bash
# 构建
docker build -t sensortower-mcp .

# 运行（双 Token）
docker run --rm \
  -e SENSOR_TOWER_API_TOKEN=st_xxx \
  -e SENSOR_TOWER_API_TOKEN_BACKUP=st_yyy \
  -p 8666:8666 \
  sensortower-mcp

# Docker Compose
docker compose up -d
```

---

## 📞 获取帮助

| 资源 | 链接 |
|------|------|
| GitHub Issues | https://github.com/toller892/SensorTower_mcp/issues |
| 完整文档 | [README.zh-CN.md](README.zh-CN.md) |
| 配置指南 | [DUAL_TOKEN_GUIDE.md](DUAL_TOKEN_GUIDE.md) |
| 更新日志 | [CHANGELOG_DUAL_TOKEN.md](CHANGELOG_DUAL_TOKEN.md) |
| 原始项目 | https://github.com/virusimmortal00/sensortower-mcp |

---

## ⚡ 最佳实践

1. ✅ **始终配置备用 Token** - 确保服务高可用
2. ✅ **监控配额使用** - 避免两个 Token 同时耗尽
3. ✅ **定期轮换 Token** - 提高安全性
4. ✅ **使用 .env 文件** - 不要硬编码 Token
5. ✅ **查看启动日志** - 确认 Token 配置正确
6. ✅ **测试切换逻辑** - 运行 test_dual_token.py

---

**版本：** 1.2.10+ (Dual Token Edition)  
**更新：** 2026-01-29  
**维护：** toller892
