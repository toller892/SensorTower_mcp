# 双 Token 功能更新日志

## 版本：1.2.10+ (Dual Token Edition)

### 发布日期：2026-01-29

---

## 🎉 主要新功能

### 1. 双 API Token 支持
- 支持配置主 Token 和备用 Token
- 环境变量：`SENSOR_TOWER_API_TOKEN` 和 `SENSOR_TOWER_API_TOKEN_BACKUP`
- 命令行参数：`--token` 和 `--backup-token`

### 2. 自动故障转移
- 当主 Token 配额耗尽时自动切换到备用 Token
- 检测 HTTP 429 (Too Many Requests) 错误
- 检测 HTTP 403 (Forbidden) 配额相关错误
- 无缝切换，不中断服务

### 3. 智能错误检测
```python
# 检测配额错误的关键词
['quota', 'limit', 'exceeded', 'rate']
```

### 4. 可扩展架构
- 支持多个备用 Token（架构层面）
- 当前实现支持 1 个主 Token + 1 个备用 Token
- 可轻松扩展到更多备用 Token

---

## 📝 代码变更

### 修改的文件

#### 1. `src/sensortower_mcp/config.py`
**新增功能：**
- `get_auth_tokens()` - 获取主 Token 和备用 Token 列表
- `--backup-token` 命令行参数
- `SENSOR_TOWER_API_TOKEN_BACKUP` 环境变量支持
- 启动信息显示 Token 数量

**代码示例：**
```python
def get_auth_tokens(primary_token: Optional[str] = None, 
                   backup_token: Optional[str] = None) -> List[str]:
    tokens = []
    primary = primary_token or os.getenv("SENSOR_TOWER_API_TOKEN")
    if primary:
        tokens.append(primary)
    backup = backup_token or os.getenv("SENSOR_TOWER_API_TOKEN_BACKUP")
    if backup:
        tokens.append(backup)
    return tokens
```

#### 2. `src/sensortower_mcp/base.py`
**新增功能：**
- `backup_tokens` 参数支持
- `current_token_index` 跟踪当前使用的 Token
- `switch_to_backup_token()` 方法实现 Token 切换
- 增强的 `make_request()` 方法，支持自动切换

**核心逻辑：**
```python
def switch_to_backup_token(self) -> bool:
    if self.current_token_index < len(self.all_tokens) - 1:
        self.current_token_index += 1
        print(f"⚠️  Switching to backup token #{self.current_token_index + 1}")
        return True
    return False

# 在 make_request 中检测配额错误
is_quota_error = status_code == 429
if status_code == 403:
    error_body = status_error.response.json()
    error_message = str(error_body).lower()
    is_quota_error = any(keyword in error_message for keyword in 
                       ['quota', 'limit', 'exceeded', 'rate'])

if is_quota_error and self.switch_to_backup_token():
    params["auth_token"] = self.get_auth_token()
    continue
```

#### 3. `src/sensortower_mcp/server.py`
**新增功能：**
- 导入 `get_auth_tokens` 函数
- 更新 `setup_client()` 返回 Token 列表
- 更新 `register_all_tools()` 接受 Token 列表
- 将 Token 列表传递给所有工具类

**初始化示例：**
```python
primary_token = tokens[0]
backup_tokens = tokens[1:] if len(tokens) > 1 else []

app_analysis = AppAnalysisTools(self.client, primary_token, backup_tokens)
```

---

## 📚 新增文档

### 1. `DUAL_TOKEN_GUIDE.md`
- 完整的配置指南
- 工作原理说明
- 故障排除指南
- 最佳实践建议

### 2. `README.zh-CN.md`
- 中文版完整文档
- 快速开始指南
- 配置示例
- 常见问题解答

### 3. `mcp-config-examples.json`
- Cursor IDE 配置
- Claude Desktop 配置
- Kiro IDE 配置
- HTTP 模式配置
- Windows Python Launcher 配置

### 4. `.env.local.example`
- 详细的环境变量配置示例
- 包含使用说明和注释

### 5. `start_server.bat`
- Windows 一键启动脚本
- 自动检查 Python 环境
- 验证 .env 文件存在

### 6. `test_dual_token.py`
- Token 切换逻辑测试
- 独立运行，无需外部依赖
- 验证所有切换场景

---

## 🔄 更新的文档

### 1. `README.md`
**新增内容：**
- 备用 Token 配置说明
- 自动故障转移功能介绍
- 双 Token 配置示例
- Docker 双 Token 支持

### 2. `.env.example`
**新增内容：**
- `SENSOR_TOWER_API_TOKEN_BACKUP` 配置项
- 详细的注释说明

---

## 🧪 测试

### 测试脚本：`test_dual_token.py`

**测试场景：**
1. ✅ 初始使用主 Token
2. ✅ 切换到第一个备用 Token
3. ✅ 切换到第二个备用 Token（如果有）
4. ✅ 无更多 Token 时保持当前 Token
5. ✅ 无备用 Token 时的行为

**运行测试：**
```bash
py -3.13 test_dual_token.py
```

**预期输出：**
```
🧪 Testing Token Failover Mechanism

✓ Initial token: st_primary_token_123
✓ Switching to backup token...
⚠️  Switching to backup token #2
✓ Now using: st_backup_token_456
✓ Switching to second backup token...
⚠️  Switching to backup token #3
✓ Now using: st_backup_token_789
✓ Attempting to switch beyond available tokens...
✓ Correctly stayed at last token: st_backup_token_789

✓ Testing tool with no backup tokens...
✓ Correctly cannot switch when no backup available

✅ All token failover tests passed!
```

---

## 🚀 使用示例

### 基本配置

```bash
# .env 文件
SENSOR_TOWER_API_TOKEN=st_primary_token_xxx
SENSOR_TOWER_API_TOKEN_BACKUP=st_backup_token_yyy
```

### 启动服务器

```bash
# 方法 1: 使用启动脚本（Windows）
start_server.bat

# 方法 2: 命令行
py -3.13 -m sensortower_mcp.server

# 方法 3: 带参数
py -3.13 -m sensortower_mcp.server --token st_xxx --backup-token st_yyy
```

### MCP 客户端配置

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

---

## 📊 运行时行为

### 启动日志

```
🚀 Starting Sensor Tower MCP Server (FastMCP)
📡 API Base URL: https://api.sensortower.com
🚌 Transport: stdio
🔧 Available tools: 40
🔑 API Tokens configured: 2 (Primary + Backup)
```

### Token 切换日志

```
⚠️  Switching to backup token #2
🔄 Retrying request with backup token...
```

---

## ⚠️ 重要说明

### 1. Token 不会自动重置
- 切换到备用 Token 后，不会自动切回主 Token
- 需要重启服务器才能重置到主 Token
- 这是设计行为，避免频繁切换

### 2. 配额管理建议
- 监控两个 Token 的配额使用情况
- 避免两个 Token 同时耗尽
- 考虑使用不同的配额计划
- 设置配额告警通知

### 3. 安全性
- 不要将 Token 提交到版本控制
- 使用 `.env` 文件并确保在 `.gitignore` 中
- 定期轮换 API Token
- 为不同环境使用不同的 Token

---

## 🔮 未来计划

### 可能的增强功能

1. **Token 池管理**
   - 支持 3+ 个 Token
   - 循环使用策略
   - Token 健康检查

2. **智能切换**
   - 基于配额剩余量预测性切换
   - Token 使用统计
   - 自动负载均衡

3. **监控和告警**
   - Token 使用率监控
   - 配额告警通知
   - 切换事件日志

4. **配置增强**
   - 支持配置文件
   - Token 优先级设置
   - 自定义切换策略

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

如果你有任何建议或发现问题，请在 GitHub 上创建 Issue：
https://github.com/toller892/SensorTower_mcp/issues

---

## 📄 许可证

本项目基于原始项目 [virusimmortal00/sensortower-mcp](https://github.com/virusimmortal00/sensortower-mcp) 进行修改。

---

## 🙏 致谢

- 感谢 [virusimmortal00](https://github.com/virusimmortal00) 创建原始项目
- 感谢 FastMCP 框架提供的强大功能
- 感谢 Sensor Tower 提供的 API 服务

---

**更新时间：** 2026-01-29  
**版本：** 1.2.10+ (Dual Token Edition)  
**维护者：** toller892
