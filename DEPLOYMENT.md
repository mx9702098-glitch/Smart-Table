# 善治美系统部署指南

## 🚀 GitHub Pages 部署步骤

### 1. 手动启用 GitHub Pages

由于GitHub Pages需要手动启用，请按以下步骤操作：

1. **访问仓库设置**
   - 打开 https://github.com/mx9702098-glitch/-
   - 点击仓库页面顶部的 "Settings" 标签

2. **启用 Pages 功能**
   - 在左侧菜单中找到 "Pages" 选项
   - 在 "Source" 部分选择 "GitHub Actions"
   - 点击 "Save" 保存设置

3. **等待自动部署**
   - 设置完成后，GitHub Actions 会自动运行
   - 部署完成后，您的网站将在以下地址可用：
   - `https://mx9702098-glitch.github.io/-/`

### 2. 访问地址

- **主页面**: https://mx9702098-glitch.github.io/-/index.html
- **移动端版本**: https://mx9702098-glitch.github.io/-/shan-zhi-mei-mobile.html

### 3. 本地测试

如果您想在本地测试，可以运行：

```bash
# 启动本地服务器
python3 -m http.server 8080

# 或者使用项目提供的部署脚本
./deploy.sh
```

然后访问 http://localhost:8080

### 4. 故障排除

如果遇到部署问题：

1. **检查 GitHub Pages 设置**
   - 确保在仓库设置中启用了 Pages
   - 确保选择了 "GitHub Actions" 作为源

2. **查看 Actions 日志**
   - 在仓库页面点击 "Actions" 标签
   - 查看最新的工作流运行日志

3. **重新触发部署**
   - 推送新的提交到 main 分支
   - 或在 Actions 页面手动重新运行工作流

## 📱 功能特色

- ✅ 移动端优先的响应式设计
- ✅ 村两委和村民双角色界面
- ✅ 完整的六步数字化工作流程
- ✅ 智能数据预填和OCR识别模拟
- ✅ 任务看板和进度管理
- ✅ 现代化的用户界面设计

## 🔧 技术栈

- **前端**: HTML5 + CSS3 + JavaScript
- **样式**: 响应式设计，移动端优化
- **图标**: Font Awesome
- **部署**: GitHub Pages + GitHub Actions