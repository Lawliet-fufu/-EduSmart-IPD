# Gitee Deployment Guide | Gitee 部署指南

This guide details how to deploy the EduSmart Platform to Gitee.
本指南详细说明如何将 EduSmart 智能家校教学平台部署到 Gitee。

---

## 📋 Preparation | 部署前准备

### 1. Check Files | 检查文件

Ensure the following files are ready:
确保以下文件已准备好：

```bash
README.md          # Project Documentation | 项目说明
CHANGELOG.md       # Change Logs | 更新日志
.gitignore         # Git Ignore File | Git忽略文件
LICENSE            # License (Optional) | 开源协议（可选）
```

### 2. Check .gitignore | 检查 .gitignore

Confirm `.gitignore` includes validity checks:
确认 `.gitignore` 包含以下内容：

```gitignore
# Dependencies
node_modules/
__pycache__/
*.pyc
venv/
env/

# Build Output
dist/
build/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment Variables
.env
.env.local

# System Files
.DS_Store
Thumbs.db
```

---

## 🚀 Deployment Steps | 部署步骤

### Step 1: Create Gitee Repository | 创建Gitee仓库

1. Login to [Gitee](https://gitee.com/)
   登录 [Gitee](https://gitee.com/)
2. Click "+" top right → "New Repository"
   点击右上角 "+" → "新建仓库"
3. Fill information | 填写信息:
   - **Repository Name**: `edu-smart-platform`
   - **Description**: `Smart Home-School Platform - Vue3 + Flask`
   - **Access**: Public or Private (`公开` 或 `私有`)
   - **Initialize**: Unchecked (We have code) | 不勾选
4. Click "Create" | 点击"创建"

### Step 2: Initialize Local Repository | 初始化本地仓库

```bash
# Execute in project root
# 在项目根目录执行
cd path/to/project

# Initialize Git
# 初始化Git仓库
git init

# Add all files
# 添加所有文件
git add .

# Commit
# 提交
git commit -m "feat: v1.1.0 - UI enhancements and role-based system"
```

### Step 3: Link Gitee Repository | 关联Gitee仓库

```bash
# Add remote (Replace with your username)
# 添加远程仓库（替换为你的用户名）
git remote add origin https://gitee.com/your-username/edu-smart-platform.git

# Verify remote
# 查看远程仓库
git remote -v
```

### Step 4: Push Code | 推送代码

```bash
# Push to main branch
# 推送到main分支
git push -u origin main

# Force push if needed (First time)
# 如果推送失败，可能需要强制推送（首次）
git push -u origin main --force
```

---

## 📦 Branch Management | 分支管理

### Create Development Branch | 创建开发分支

```bash
# Create develop branch
# 创建develop分支
git checkout -b develop
git push -u origin develop

# Create feature branch
# 创建功能分支
git checkout -b feature/new-feature
```

### Branch Strategy | 分支策略

```
main (Production/生产)
  ↑
  └── develop (Development/开发)
       ├── feature/xxx (Feature/功能)
       ├── bugfix/xxx (Fix/修复)
       └── hotfix/xxx (Urgent Fix/紧急修复)
```

---

## 🏷️ Version Tags | 版本标签

### Create Tags | 创建标签

```bash
# Create v1.1.0 tag
# 创建v1.1.0标签
git tag -a v1.1.0 -m "Release v1.1.0: UI enhancements and role system"

# Push tag
# 推送标签
git push origin v1.1.0

# Push all tags
# 推送所有标签
git push origin --tags
```

---

## 📝 Commit Convention | 提交规范

### Format | 格式

```bash
<type>(<scope>): <subject>

# Example | 示例
feat(auth): add role-based access control
fix(ui): resolve sidebar color issue
docs: update README with deployment guide
style(sidebar): apply dark green theme
refactor(views): convert TypeScript to JavaScript
```

### Types | 类型

- `feat`: New Feature | 新功能
- `fix`: Bug Fix | Bug修复
- `docs`: Documentation | 文档
- `style`: Styles | 样式
- `refactor`: Refactor | 重构
- `test`: Tests | 测试
- `chore`: Build/Tools | 构建/工具

---

## 🔄 Update Workflow | 日常更新流程

### 1. Pull Latest Code | 拉取最新代码

```bash
git pull origin main
```

### 2. Create Feature Branch | 创建功能分支

```bash
git checkout -b feature/your-feature
```

### 3. Develop & Commit | 开发并提交

```bash
git add .
git commit -m "feat(module): add new feature"
```

### 4. Push Branch | 推送分支

```bash
git push origin feature/your-feature
```

### 5. Create Pull Request | 创建Pull Request

1. Visit Repository Page | 访问仓库页面
2. Click "Pull Requests" | 点击 "Pull Requests"
3. Click "New Pull Request" | 点击 "新建 Pull Request"
4. Select Branch: `feature/your-feature` → `main`
5. Submit | 提交

---

## 🌐 Gitee Pages (Optional) | Gitee Pages部署（可选）

### Enable Pages | 启用Pages服务

1. Repository → "Services" → "Gitee Pages"
   进入仓库 → "服务" → "Gitee Pages"
2. Branch: `main`
3. Directory: `frontend/dist` (Run `npm run build` first)
4. Click "Start" | 点击"启动"

### Build Frontend | 构建前端

```bash
cd frontend
npm run build
```

The output files are in `frontend/dist/`.
生成的文件在 `frontend/dist/`。

---

## ⚙️ Env Configuration | 环境配置

### Create .env File | 创建 .env 文件

```bash
# frontend/.env.production
VITE_API_URL=https://your-backend-url.com
```

> **Note**: Do not commit `.env` to Git.
> **注意**: `.env` 文件不要提交到Git。

---

## 🔐 Security | 安全建议

### Sensitive Info | 敏感信息管理

1. **Do Not Commit | 不要提交**:
   - Database Passwords | 数据库密码
   - API Keys | API密钥
   - JWT Secrets | JWT密钥
   - `.env` files

2. **Use Environment Variables | 使用环境变量**:
   ```bash
   # Set env vars on server
   # 在服务器设置环境变量
   export DATABASE_URL=xxx
   export SECRET_KEY=xxx
   ```

---

## 🤝 Collaboration | 团队协作

### Invite Members | 邀请成员

1. Settings → Members | 仓库设置 → 成员管理
2. Enter username | 输入成员用户名
3. Set Permission | 设置权限（Owner/Developer/Reporter）

---

## ❓ FAQ | 常见问题

### Q: Permission denied?
```bash
# Check SSH Key
# 检查SSH密钥配置
ssh -T git@gitee.com

# Or use HTTPS
# 或使用HTTPS并输入账号密码
git remote set-url origin https://gitee.com/your-username/edu-smart-platform.git
```

### Q: Undo last commit? | 撤销最后一次提交?
```bash
# Keep changes | 保留更改
git reset --soft HEAD^

# Discard changes | 丢弃更改
git reset --hard HEAD^
```

### Q: Resolve conflicts? | 解决合并冲突?
```bash
# 1. Pull latest
# 1. 拉取最新代码
git pull origin main

# 2. Resolve manually
# 2. 手动解决冲突文件
# 3. Mark resolved
# 3. 标记已解决
git add .

# 4. Commit
# 4. 提交
git commit -m "fix: resolve merge conflicts"
```

---

**Good luck with deployment! | 祝部署顺利！**
