#!/bin/bash

# 善治美项目部署脚本
echo "🚀 正在启动善治美数字化村务管理平台..."

# 检查Python是否可用
if command -v python3 &> /dev/null; then
    echo "✅ Python3 已安装"
    echo "📡 启动HTTP服务器 (端口: 8080)..."
    echo "🌐 访问地址: http://localhost:8080"
    echo "📱 移动端应用: http://localhost:8080/shan-zhi-mei-mobile.html"
    echo ""
    echo "按 Ctrl+C 停止服务器"
    echo "=================================="
    python3 -m http.server 8080
elif command -v python &> /dev/null; then
    echo "✅ Python 已安装"
    echo "📡 启动HTTP服务器 (端口: 8080)..."
    echo "🌐 访问地址: http://localhost:8080"
    echo "📱 移动端应用: http://localhost:8080/shan-zhi-mei-mobile.html"
    echo ""
    echo "按 Ctrl+C 停止服务器"
    echo "=================================="
    python -m http.server 8080
else
    echo "❌ 未找到Python，请安装Python后重试"
    exit 1
fi