# 双 Token 自动切换功能指南

## 功能概述

Sensor Tower MCP Server 现在支持配置备用 API Token，当主 Token 的配额用完时，系统会自动切换到备用 Token，确保服务不中断。

## 配置方法

### 方法 1: 环境变量（推荐）

在 `.env` 文件中配置：

```bash
# 主 Token（必需）
SENSOR_TOWER_API_TOKEN=st_your_primary_token_here

# 备用 Token（可选）
SENSOR_TOWER_API_TOKEN_BACKUP=st_your_backup_token_here
```

### 方法 2: 命令行参数

```bash
python -m sensortower_mcp.server \
  --token st_your_primary_token \
  --backup-token st_your_backup_token
```

### 方法 3: MCP 客户端配置

#### Cursor / Claude Desktop

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

#### Docker

```bash
docker run --rm \
  -e SENSOR_TOWER_API_TOKEN=st_primary_token \
  -e SENSOR_TOWER_API_TOKEN_BACKUP=st_backup_token \
  -p 8666:8666 \
  sensortower-mcp
```

## 工作原理

1. **正常运行**: 服务器使用主 Token 处理所有 API 请求

2. **检测配额耗尽**: 当 API 返回以下错误时触发切换：
   - HTTP 429 (Too Many Requests)
   - HTTP 403 (Forbidden) 且错误信息包含 'quota', 'limit', 'exceeded', 'rate' 等关键词

3. **自动切换**: 系统自动切换到备用 Token，并在控制台输出：
   ```
   ⚠️  Switching to backup token #2
   🔄 Retrying request with backup token...
   ```

4. **继续服务**: 所有后续请求使用备用 Token，无需重启服务器

## 启动信息

配置双 Token 后，启动时会显示：

```
🚀 Starting Sensor Tower MCP Server (FastMCP)
📡 API Base URL: https://api.sensortower.com
🚌 Transport: stdio
🔧 Available tools: 40
🔑 API Tokens configured: 2 (Primary + Backup)
```

## 支持多个备用 Token

虽然当前配置只支持一个备用 Token，但代码架构支持扩展到多个备用 Token。如需添加更多备用 Token，可以修改 `config.py` 中的 `get_auth_tokens` 函数。

## 注意事项

1. **Token 不会自动重置**: 一旦切换到备用 Token，除非重启服务器，否则会一直使用备用 Token

2. **配额管理**: 建议监控两个 Token 的配额使用情况，避免两个都耗尽

3. **安全性**: 
   - 不要将 Token 提交到版本控制系统
   - 使用 `.env` 文件并确保它在 `.gitignore` 中
   - 定期轮换 API Token

4. **测试**: 使用 `test_dual_token.py` 脚本验证切换逻辑：
   ```bash
   py -3.13 test_dual_token.py
   ```

## 故障排除

### 问题: 备用 Token 没有生效

**检查项**:
- 确认环境变量名称正确：`SENSOR_TOWER_API_TOKEN_BACKUP`
- 检查 Token 格式是否正确（以 `st_` 开头）
- 查看服务器启动日志，确认显示 "API Tokens configured: 2"

### 问题: 切换后仍然报错

**可能原因**:
- 备用 Token 也已达到配额限制
- 备用 Token 无效或已过期
- API 返回的是其他类型的错误（非配额相关）

**解决方法**:
- 检查两个 Token 的配额状态
- 在 Sensor Tower 控制台验证 Token 有效性
- 查看详细错误日志确定具体问题

## 最佳实践

1. **配额分配**: 为主 Token 和备用 Token 分配不同的配额计划，确保总配额充足

2. **监控告警**: 设置配额使用监控，在接近限制时收到通知

3. **定期检查**: 定期验证两个 Token 都处于有效状态

4. **日志记录**: 关注服务器日志中的切换消息，了解配额使用模式

## 技术细节

### 修改的文件

- `src/sensortower_mcp/config.py`: 添加备用 Token 配置支持
- `src/sensortower_mcp/base.py`: 实现自动切换逻辑
- `src/sensortower_mcp/server.py`: 更新服务器初始化流程
- `.env.example`: 添加配置示例
- `README.md`: 更新文档

### 切换逻辑代码

```python
def switch_to_backup_token(self) -> bool:
    """Switch to next available backup token"""
    if self.current_token_index < len(self.all_tokens) - 1:
        self.current_token_index += 1
        print(f"⚠️  Switching to backup token #{self.current_token_index + 1}")
        return True
    return False
```

### 错误检测代码

```python
# Check if it's a quota/rate limit error
is_quota_error = status_code == 429
if status_code == 403:
    error_body = status_error.response.json()
    error_message = str(error_body).lower()
    is_quota_error = any(keyword in error_message for keyword in 
                       ['quota', 'limit', 'exceeded', 'rate'])

# If quota error and we have backup tokens, try switching
if is_quota_error and self.switch_to_backup_token():
    params["auth_token"] = self.get_auth_token()
    continue
```

## 获取 API Token

访问 Sensor Tower 控制台获取 API Token：
https://app.sensortower.com/users/edit/api-settings

建议为不同的 Token 设置不同的名称，便于管理和追踪使用情况。
