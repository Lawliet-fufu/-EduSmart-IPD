# Changelog | 更新日志

All notable changes to this project will be documented in this file.
所有值得注意的项目更改都将记录在此文件中。

---

## [1.2.0] - 2025-12-18

### ✨ New Features | 新增功能

#### Notices System | 通知公告系统
- **Complete CRUD Operations | 完整的增删改查功能**
  - Display notices from database | 展示数据库中的通知信息
  - Create new notices with role-based permissions | 基于角色权限创建通知
  - Edit and delete notices | 编辑和删除通知功能
  - Filter by priority and category | 按优先级和类别筛选

#### Backend API Enhancements | 后端API增强
- **Notice Management API | 通知管理API**
  - `GET /api/admin/notices` - Fetch all notices with filters | 获取通知列表（支持过滤）
  - `GET /api/admin/notices/:id` - Get single notice details | 获取单个通知详情
  - `POST /api/admin/notices` - Create notice (Admin/Teacher only) | 创建通知（仅管理员/教师）
  - `PUT /api/admin/notices/:id` - Update notice | 更新通知
  - `DELETE /api/admin/notices/:id` - Delete notice | 删除通知

- **Authentication System | 认证系统**
  - JWT token-based authentication | 基于JWT的身份认证
  - Role-based access control | 基于角色的访问控制
  - Secure password verification | 安全密码验证
  - Database connection error handling | 数据库连接错误处理

### 🎨 Frontend Improvements | 前端改进

#### NoticesView Component | 通知页面组件
- **Data Display | 数据展示**
  - Real-time database synchronization | 实时数据库同步
  - Notice cards with priority indicators | 带优先级指示的通知卡片
  - Author information display | 作者信息展示
  - Date formatting and metadata | 日期格式化和元数据展示

- **Interactive Features | 交互功能**
  - Create/Edit modal dialogs | 创建/编辑模态框
  - View notice details modal | 查看通知详情模态框
  - Form validation | 表单验证
  - Loading and error states | 加载和错误状态处理

- **Permission Control | 权限控制**
  - Role-based button visibility | 基于角色的按钮可见性
  - Author-only edit/delete permissions | 仅作者可编辑/删除

#### API Layer | API层
- **notices.js Module | 通知API模块**
  - Modular API functions | 模块化API函数
  - Parameter filtering support | 参数过滤支持
  - RESTful endpoint integration | RESTful端点集成
  - Error handling and response parsing | 错误处理和响应解析

### 🔧 Technical Implementations | 技术实现

#### Backend Files Modified | 后端修改文件
- **admin_mgmt_views.py**
  - Complete notice CRUD endpoints | 完整的通知CRUD端点
  - Role-based decorators (`@role_required`) | 基于角色的装饰器
  - Database query optimization | 数据库查询优化
  - Author information join queries | 作者信息关联查询

- **auth_views.py**
  - Login endpoint with JWT generation | 登录端点及JWT生成
  - User information retrieval | 用户信息获取
  - Database error handling | 数据库错误处理
  - Password verification logic | 密码验证逻辑

#### Frontend Files Modified | 前端修改文件
- **NoticesView.vue**
  - Vue 3 Composition API implementation | Vue 3组合式API实现
  - Reactive state management | 响应式状态管理
  - Modal dialogs for CRUD operations | CRUD操作的模态框
  - Priority color coding system | 优先级颜色编码系统
  - Lucide icons integration | Lucide图标集成

- **notices.js**
  - Axios-based API service layer | 基于Axios的API服务层
  - RESTful method wrappers | RESTful方法封装
  - Request/response interceptors | 请求/响应拦截器
  - Filter parameters support | 过滤参数支持

### 🐛 Bug Fixes | Bug修复

- Fixed 404 error on `/api/admin/notices` endpoint | 修复通知API端点404错误
- Fixed OPTIONS request handling for CORS | 修复CORS预检请求处理
- Fixed notice data not displaying on frontend | 修复前端无法显示通知数据
- Fixed database connection error messages | 修复数据库连接错误信息

### 📦 Database Integration | 数据库集成

- Connected Notice model to MySQL database | 通知模型连接到MySQL数据库
- Implemented proper foreign key relationships | 实现正确的外键关系
- Added author-user relationship queries | 添加作者-用户关系查询
- Proper transaction handling and rollback | 正确的事务处理和回滚

---

## [1.1.0] - 2025-12-01

### ✨ New Features | 新增功能

#### UI/UX Enhancements | UI/UX 增强
- **Dark Green Sidebar | 深绿色主题侧边栏**
  - Vertical gradient effect | 垂直渐变效果 (#047857 → #065f46 → #064e3b)
  - Semi-transparent border & Deep shadow | 半透明绿色边框 & 深度阴影效果
  
- **Soft Green Background | 柔和绿色背景**
  - Geometric pattern overlay | 几何图案叠加层
  - Fixed positioning | 固定定位，所有页面生效
  
- **Optimized Login | 优化登录界面**
  - Quick role selection cards | 三个角色快速选择卡片 (Admin/Teacher/Student)
  - Unified Lucide icons style | 统一的Lucide图标风格
  - Light gray selection state | 浅灰色选中状态

#### Role-Based System | 角色权限系统
- **Three Roles Implementation | 三角色实现**
  - **Admin**: Full access permissions | 所有功能权限
  - **Teacher**: 5 functional permissions | 5个功能权限
  - **Student**: 3 basic functional permissions | 3个基础功能权限
  
- **Permission Control | 权限控制**
  - Menu filtering based on roles | 基于角色的菜单过滤
  - Local storage for role info | 角色信息本地存储

#### AI Assistant Extensions | AI助手功能扩展
- **File Upload | 文件上传**
  - Support PDF, PPT, DOC formats | 支持多种文档格式
  - Auto-analysis display | 文件信息自动分析展示
  
- **Mind Map Generation | 思维导图生成**
  - Visual course structure | 可视化课程结构
  - Auto-layout algorithm | 自动布局算法
  
- **Courseware Analysis | 课件分析**
  - Key topic extraction | 关键主题提取
  - Learning objective analysis | 学习目标分析

### 🎨 Style Improvements | 样式改进

#### Sidebar | 侧边栏
- New gradient background | 深绿色渐变背景替代浅灰色
- Translucent logo with glow | Logo图标半透明设计 + 发光效果
- Selected state: 30% green bg | 选中状态：30%绿色背景 + 白色文字

#### Main Content | 主内容区
- Light green background (75% opacity) | 浅绿色背景（75%不透明度）
- Enhanced white cards | 白色卡片更突出

#### Icons | 图标系统
- Unified Lucide Icons | 全部使用Lucide Icons
- Removed emoji icons | 移除emoji图标，统一风格

### 🔧 Technical Improvements | 技术改进

- **Removed TypeScript | 完全移除TypeScript**
  - All `.ts` files converted to `.js` | 所有 `.ts` 文件转换为 `.js`
  - Removed type annotations | 移除类型注解
  
- **State Management | State管理增强**
  - Added role enums in `auth.js` | `auth.js` 添加角色枚举
  - Added computed properties for roles | 新增角色计算属性

### 🐛 Bug Fixes | Bug修复

- Fixed token persistence issue | 修复登录后token未保存问题
- Fixed style file corruption | 修复样式文件损坏问题
- Fixed sidebar permission logic | 修复Sidebar菜单权限过滤逻辑
- Fixed CSS variable references | 修复CSS变量引用错误

---

## [1.0.0] - 2025-11-26

### ✨ Initial Release | 初始发布

#### Core Features | 核心功能
- Authentication System | 用户认证系统
- Dashboard & Notices | 仪表板页面 & 通知公告模块
- Assignment Management | 作业管理模块
- Class Management | 班级管理模块
- AI Teaching Assistant | AI教学助手
- Settings Page | 设置页面

#### Tech Stack | 技术架构
- **Frontend**: Vue 3 + Vite + Pinia + Vue Router
- **Backend**: Flask + SQLAlchemy
- **Icons**: Lucide Vue Next
- **Styles**: Native CSS + Variables

#### UI Design | UI设计
- Modern Card Layout | 现代化卡片式布局
- Responsive Design | 响应式设计
- Unified Green Theme | 统一的绿色主题

---

## Versions | 版本计划

### [1.3.0] - Planned | 计划中

#### Features | 功能
- [ ] Real-time Notifications | 实时通知系统
- [ ] Email Notification Service | 邮件通知服务
- [ ] Notice Read Status Tracking | 通知阅读状态追踪
- [ ] Attachment Support for Notices | 通知附件支持

### [1.2.0] - Planned | 计划中

#### Features | 功能
- [x] Complete Backend API | 后端API完整实现
- [x] Database Integration | 数据库集成
- [ ] Real File Upload | 真实文件上传
- [ ] Real-time Notifications | 实时通知系统

#### Improvements | 优化
- [ ] Mobile Optimization | 移动端适配优化
- [ ] Dark Mode | 暗黑模式主题
- [ ] Performance Tuning | 性能优化
- [ ] SEO Optimization | SEO优化

---

## Types | 类型说明

- `feat`: New feature | 新功能
- `fix`: Bug fix | Bug修复
- `docs`: Documentation | 文档更新
- `style`: Styles | 样式改进
- `refactor`: Refactoring | 代码重构
- `perf`: Performance | 性能优化
- `test`: Tests | 测试相关
- `chore`: Build/Tools | 构建/工具链

---

**Note**: SemVer is followed.
**注**: 版本遵循语义化版本。
