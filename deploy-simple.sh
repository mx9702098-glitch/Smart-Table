#!/bin/bash

echo "🚀 善治美系统 - 简单部署脚本"
echo "================================"

# 检查是否在正确的目录
if [ ! -f "index.html" ]; then
    echo "❌ 错误：未找到 index.html 文件"
    echo "请确保在项目根目录运行此脚本"
    exit 1
fi

echo "✅ 项目文件检查完成"

# 创建 gh-pages 分支并部署
echo "📦 创建 gh-pages 分支..."

# 删除可能存在的 gh-pages 分支
git branch -D gh-pages 2>/dev/null || true

# 创建新的 gh-pages 分支
git checkout --orphan gh-pages

# 添加所有文件
git add .

# 提交
git commit -m "部署善治美系统到 GitHub Pages"

# 推送到远程 gh-pages 分支
echo "🚀 推送到 GitHub Pages..."
git push -f origin gh-pages

# 切换回 main 分支
git checkout main

echo ""
echo "🎉 部署完成！"
echo "================================"
echo "现在请按以下步骤启用 GitHub Pages："
echo ""
echo "1. 访问: https://github.com/mx9702098-glitch/-/settings/pages"
echo "2. 在 'Source' 部分选择 'Deploy from a branch'"
echo "3. 选择 'gh-pages' 分支"
echo "4. 选择 '/ (root)' 文件夹"
echo "5. 点击 'Save'"
echo ""
echo "几分钟后，您的网站将在以下地址可用："
echo "https://mx9702098-glitch.github.io/-/"
echo ""