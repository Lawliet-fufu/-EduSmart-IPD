# Gitee 部署指南

本指南详细说明如何将 EduSmart 智能家校教学平台部署到 Gitee。

---

## 📋 部署前准备

### 1. 检查文件

确保以下文件已准备好：

```bash
✅ README.md          # 项目说明
✅ CHANGELOG.md       # 更新日志
✅ .gitignore         # Git忽略文件
✅ LICENSE            # 开源协议（可选）
```

### 2. 检查 .gitignore

确认 `.gitignore` 包含以下内容：

```gitignore
# 依赖
node_modules/
__pycache__/
*.pyc
venv/
env/

# 构建产物
dist/
build/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# 环境变量
.env
.env.local

# 系统文件
.DS_Store
Thumbs.db
```

---

## 🚀 部署步骤

### 步骤 1: 创建Gitee仓库

1. 登录 [Gitee](https://gitee.com/)
2. 点击右上角 "+" → "新建仓库"
3. 填写信息：
   - **仓库名称**: `edu-smart-platform`
   - **仓库介绍**: `智能家校教学平台 - Vue3 + Flask`
   - **是否开源**: 选择"公开"或"私有"
   - **初始化仓库**: 不勾选（我们已有代码）
4. 点击"创建"

### 步骤 2: 初始化本地仓库

```bash
# 在项目根目录执行
cd c:\Users\Lawliet\.gemini\antigravity-browser-profile\IPD

# 初始化Git仓库（如果还没初始化）
git init

# 添加所有文件
git add .

# 提交
git commit -m "feat: v1.1.0 - UI enhancements and role-based system"
```

### 步骤 3: 关联Gitee仓库

```bash
# 添加远程仓库（替换为你的用户名）
git remote add origin https://gitee.com/your-username/edu-smart-platform.git

# 查看远程仓库
git remote -v
```

### 步骤 4: 推送代码

```bash
# 推送到main分支
git push -u origin main

# 如果推送失败，可能需要强制推送（首次）
git push -u origin main --force
```

---

## 📦 分支管理

### 创建开发分支

```bash
# 创建develop分支
git checkout -b develop
git push -u origin develop

# 创建功能分支
git checkout -b feature/new-feature
```

### 分支策略

```
main (生产)
  ↑
  └── develop (开发)
       ├── feature/xxx (功能)
       ├── bugfix/xxx (修复)
       └── hotfix/xxx (紧急修复)
```

---

## 🏷️ 版本标签

### 创建版本标签

```bash
# 创建v1.1.0标签
git tag -a v1.1.0 -m "Release v1.1.0: UI enhancements and role system"

# 推送标签
git push origin v1.1.0

# 推送所有标签
git push origin --tags
```

---

## 📝 提交规范

### Commit Message格式

```bash
<type>(<scope>): <subject>

# 示例
feat(auth): add role-based access control
fix(ui): resolve sidebar color issue
docs: update README with deployment guide
style(sidebar): apply dark green theme
refactor(views): convert TypeScript to JavaScript
```

### Type类型

- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档
- `style`: 样式
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具

---

## 🔄 日常更新流程

### 1. 拉取最新代码

```bash
git pull origin main
```

### 2. 创建功能分支

```bash
git checkout -b feature/your-feature
```

### 3. 开发并提交

```bash
git add .
git commit -m "feat(module): add new feature"
```

### 4. 推送分支

```bash
git push origin feature/your-feature
```

### 5. 在Gitee上创建Pull Request

1. 访问仓库页面
2. 点击 "Pull Requests"
3. 点击 "新建 Pull Request"
4. 选择分支: `feature/your-feature` → `main`
5. 填写说明并提交

---

## 🌐 Gitee Pages部署（可选）

### 启用Pages服务

1. 进入仓库 → "服务" → "Gitee Pages"
2. 选择分支: `main`
3. 选择目录: `frontend/dist`（需先执行 `npm run build`）
4. 点击"启动"

### 构建前端

```bash
cd frontend
npm run build
```

生成的文件在 `frontend/dist/`

---

## ⚙️ 环境配置

### 创建 .env 文件

```bash
# frontend/.env.production
VITE_API_URL=https://your-backend-url.com
```

**注意**: `.env` 文件不要提交到Git

---

## 🔐 安全建议

### 敏感信息管理

1. **不要提交**:
   - 数据库密码
   - API密钥
   - JWT密钥
   - `.env` 文件

2. **使用环境变量**:
   ```bash
   # 在服务器设置环境变量
   export DATABASE_URL=xxx
   export SECRET_KEY=xxx
   ```

---

## 📊 仓库统计

### 添加徽章

在README.md中添加：

```markdown
[![Gitee Stars](https://gitee.com/your-username/edu-smart-platform/badge/star.svg)](https://gitee.com/your-username/edu-smart-platform)
[![Gitee Forks](https://gitee.com/your-username/edu-smart-platform/badge/fork.svg)](https://gitee.com/your-username/edu-smart-platform)
```

---

## 🤝 团队协作

### 邀请成员

1. 仓库设置 → 成员管理
2. 输入成员Gitee用户名
3. 设置权限（Owner/Developer/Reporter）

### 权限说明

- **Owner**: 完全控制
- **Developer**: 读写权限
- **Reporter**: 只读权限

---

## ❓ 常见问题

### Q: 推送失败 permission denied?
```bash
# 检查SSH密钥配置
ssh -T git@gitee.com

# 或使用HTTPS并输入账号密码
git remote set-url origin https://gitee.com/your-username/edu-smart-platform.git
```

### Q: 如何撤销最后一次提交?
```bash
# 保留更改
git reset --soft HEAD^

# 丢弃更改
git reset --hard HEAD^
```

### Q: 如何解决合并冲突?
```bash
# 1. 拉取最新代码
git pull origin main

# 2. 手动解决冲突文件
# 3. 标记已解决
git add .

# 4. 提交
git commit -m "fix: resolve merge conflicts"
```

---

## 📧 获取帮助

- Gitee帮助中心: https://gitee.com/help
- Git教程: https://www.runoob.com/git/git-tutorial.html

---

**祝部署顺利！** 🎉
