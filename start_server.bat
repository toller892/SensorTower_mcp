@echo off
REM Sensor Tower MCP Server 启动脚本 (Windows)
REM 使用方法: start_server.bat

echo ========================================
echo Sensor Tower MCP Server 启动脚本
echo ========================================
echo.

REM 检查 .env 文件是否存在
if not exist .env (
    echo [错误] 未找到 .env 文件
    echo.
    echo 请按照以下步骤配置:
    echo 1. 复制 .env.example 为 .env
    echo 2. 编辑 .env 文件，填入你的 API Token
    echo 3. 重新运行此脚本
    echo.
    pause
    exit /b 1
)

echo [信息] 找到 .env 配置文件
echo.

REM 检查 Python 版本
echo [信息] 检查 Python 环境...
py -3.13 --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python 3.13
    echo 请安装 Python 3.13 或更高版本
    pause
    exit /b 1
)

echo [信息] Python 版本:
py -3.13 --version
echo.

REM 启动服务器
echo [信息] 启动 Sensor Tower MCP Server...
echo ========================================
echo.

py -3.13 -m sensortower_mcp.server

echo.
echo ========================================
echo 服务器已停止
echo ========================================
pause
