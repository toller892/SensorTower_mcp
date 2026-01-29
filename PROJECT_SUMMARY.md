# 🎉 Sensor Tower MCP 双 Token 版本 - 项目总结

## 📦 项目信息

- **项目名称：** Sensor Tower MCP Server (Dual Token Edition)
- **仓库地址：** https://github.com/toller892/SensorTower_mcp
- **基于项目：** https://github.com/virusimmortal00/sensortower-mcp
- **版本：** 1.2.10+ (Dual Token Edition)
- **完成日期：** 2026-01-29

---

## ✨ 核心功能

### 1. 双 API Token 自动切换
- ✅ 支持配置主 Token 和备用 Token
- ✅ 当主 Token 配额耗尽时自动切换到备用 Token
- ✅ 检测 HTTP 429 和配额相关的 403 错误
- ✅ 无缝切换，不中断服务
- ✅ 支持扩展到多个备用 Token

### 2. 配置方式
- ✅ 环境变量：`SENSOR_TOWER_API_TOKEN_BACKUP`
- ✅ 命令行参数：`--backup-token`
- ✅ MCP 客户端配置
- ✅ Docker 环境变量

---

## 📝 代码修改

### 修改的核心文件（3 个）

1. **src/sensortower_mcp/config.py**
   - 新增 `get_auth_tokens()` 函数
   - 支持备用 Token 参数
   - 更新启动信息显示

2. **src/sensortower_mcp/base.py**
   - 新增 Token 切换逻辑
   - 实现 `switch_to_backup_token()` 方法
   - 增强错误检测和重试机制

3. **src/sensortower_mcp/server.py**
   - 更新 Token 初始化流程
   - 传递 Token 列表到所有工具类
   - 支持多 Token 架构

### 更新的配置文件（2 个）

4. **README.md**
   - 添加双 Token 功能说明
   - 更新配置示例

5. **.env.example**
   - 添加备用 Token 配置项

---

## 📚 新增文档（8 个）

### 核心文档

1. **DUAL_TOKEN_GUIDE.md** - 双 Token 完整指南
   - 配置方法
   - 工作原理
   - 故障排除
   - 最佳实践

2. **README.zh-CN.md** - 中文完整文档
   - 快速开始
   - 功能介绍
   - 配置示例
   - 常见问题

3. **CHANGELOG_DUAL_TOKEN.md** - 详细更新日志
   - 代码变更说明
   - 新增功能列表
   - 测试场景
   - 未来计划

4. **QUICK_REFERENCE.md** - 快速参考卡片
   - 5 分钟快速开始
   - 常用命令
   - 问题速查
   - 配置模板

### 配置和示例

5. **.env.local.example** - 详细配置示例
   - 完整的环境变量说明
   - 使用指南
   - 注释说明

6. **mcp-config-examples.json** - MCP 客户端配置
   - Cursor 配置
   - Claude Desktop 配置
   - Kiro 配置
   - HTTP 模式配置

### 工具和测试

7. **start_server.bat** - Windows 启动脚本
   - 自动检查环境
   - 验证配置文件
   - 一键启动

8. **test_dual_token.py** - Token 切换测试
   - 独立测试脚本
   - 验证切换逻辑
   - 无需外部依赖

---

## 🎯 实现的功能点

### ✅ 已完成

- [x] 双 Token 配置支持
- [x] 自动故障转移机制
- [x] 配额错误检测（429, 403）
- [x] Token 切换日志输出
- [x] 多 Token 架构支持
- [x] 完整的中英文文档
- [x] MCP 客户端配置示例
- [x] Windows 启动脚本
- [x] Token 切换测试脚本
- [x] 快速参考指南
- [x] 详细更新日志
- [x] 故障排除指南

### 🔮 未来可能的增强

- [ ] Token 池管理（3+ Token）
- [ ] 循环使用策略
- [ ] Token 健康检查
- [ ] 配额使用统计
- [ ] 自动负载均衡
- [ ] 监控和告警系统
- [ ] 配置文件支持
- [ ] Token 优先级设置

---

## 📊 项目统计

### 代码变更
- **修改文件：** 5 个
- **新增文件：** 10 个
- **新增代码行：** ~500 行
- **新增文档：** ~2000 行

### Git 提交
- **总提交数：** 3 次
- **提交 1：** feat: Add dual API token support with automatic failover
- **提交 2：** docs: Add comprehensive documentation and examples
- **提交 3：** docs: Add comprehensive changelog and quick reference guide

### 文档覆盖
- ✅ 英文文档
- ✅ 中文文档
- ✅ 配置示例
- ✅ 快速参考
- ✅ 故障排除
- ✅ 最佳实践
- ✅ 测试指南

---

## 🚀 使用流程

### 1. 克隆项目
```bash
git clone https://github.com/toller892/SensorTower_mcp.git
cd SensorTower_mcp
```

### 2. 配置 Token
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 Token
```

### 3. 启动服务器
```bash
# Windows
start_server.bat

# 或命令行
py -3.13 -m sensortower_mcp.server
```

### 4. 配置 MCP 客户端
参考 `mcp-config-examples.json` 中的配置示例

---

## 🧪 测试验证

### Token 切换测试
```bash
py -3.13 test_dual_token.py
```

**测试结果：** ✅ 所有测试通过

**测试场景：**
- ✅ 初始使用主 Token
- ✅ 切换到备用 Token
- ✅ 多个备用 Token 切换
- ✅ 无更多 Token 时的行为
- ✅ 无备用 Token 时的行为

---

## 📖 文档结构

```
sensortower-mcp/
├── README.md                    # 英文主文档
├── README.zh-CN.md             # 中文完整文档
├── DUAL_TOKEN_GUIDE.md         # 双 Token 详细指南
├── CHANGELOG_DUAL_TOKEN.md     # 更新日志
├── QUICK_REFERENCE.md          # 快速参考
├── PROJECT_SUMMARY.md          # 项目总结（本文件）
├── .env.example                # 配置模板
├── .env.local.example          # 详细配置示例
├── mcp-config-examples.json    # MCP 客户端配置
├── start_server.bat            # Windows 启动脚本
├── test_dual_token.py          # Token 切换测试
└── src/
    └── sensortower_mcp/
        ├── config.py           # 配置管理（已修改）
        ├── base.py             # 基础工具类（已修改）
        └── server.py           # 服务器主程序（已修改）
```

---

## 🎓 技术亮点

### 1. 优雅的错误处理
```python
# 智能检测配额错误
is_quota_error = status_code == 429
if status_code == 403:
    error_message = str(error_body).lower()
    is_quota_error = any(keyword in error_message for keyword in 
                       ['quota', 'limit', 'exceeded', 'rate'])
```

### 2. 可扩展的架构
```python
# 支持多个备用 Token
self.all_tokens = [token] + self.backup_tokens
self.current_token_index = 0
```

### 3. 无缝切换
```python
# 自动切换并重试
if is_quota_error and self.switch_to_backup_token():
    params["auth_token"] = self.get_auth_token()
    continue
```

### 4. 清晰的日志
```python
print(f"⚠️  Switching to backup token #{self.current_token_index + 1}")
print(f"🔄 Retrying request with backup token...")
```

---

## 🌟 项目特色

1. **高可用性** - 双 Token 确保服务不中断
2. **易于配置** - 多种配置方式，灵活方便
3. **完整文档** - 中英文文档，详细示例
4. **开箱即用** - Windows 启动脚本，一键启动
5. **充分测试** - 独立测试脚本，验证功能
6. **可扩展性** - 架构支持多个备用 Token
7. **用户友好** - 清晰的日志和错误提示

---

## 🔗 相关链接

### 项目链接
- **本项目：** https://github.com/toller892/SensorTower_mcp
- **原始项目：** https://github.com/virusimmortal00/sensortower-mcp

### 文档链接
- **快速开始：** [README.zh-CN.md](README.zh-CN.md)
- **配置指南：** [DUAL_TOKEN_GUIDE.md](DUAL_TOKEN_GUIDE.md)
- **快速参考：** [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- **更新日志：** [CHANGELOG_DUAL_TOKEN.md](CHANGELOG_DUAL_TOKEN.md)

### 外部链接
- **Sensor Tower API：** https://app.sensortower.com/api/docs
- **获取 Token：** https://app.sensortower.com/users/edit/api-settings
- **FastMCP：** https://github.com/jlowin/fastmcp

---

## 🙏 致谢

- 感谢 **virusimmortal00** 创建原始项目
- 感谢 **FastMCP** 框架提供的强大功能
- 感谢 **Sensor Tower** 提供的 API 服务

---

## 📞 支持

如有问题或建议，请在 GitHub 上创建 Issue：
https://github.com/toller892/SensorTower_mcp/issues

---

## 📄 许可证

本项目基于原始项目进行修改，遵循原项目的许可证。

---

**项目完成时间：** 2026-01-29  
**版本：** 1.2.10+ (Dual Token Edition)  
**维护者：** toller892  
**状态：** ✅ 已完成并测试通过

---

## 🎊 总结

这个项目成功实现了 Sensor Tower MCP Server 的双 Token 自动切换功能，提供了：

✅ **完整的功能实现** - 自动检测配额错误并切换 Token  
✅ **详尽的文档** - 中英文文档、配置示例、快速参考  
✅ **便捷的工具** - 启动脚本、测试脚本、配置模板  
✅ **高质量代码** - 清晰的架构、优雅的错误处理  
✅ **充分测试** - 验证所有切换场景  

项目已成功推送到 GitHub，可以立即使用！🚀
