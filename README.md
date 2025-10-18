# 线索数据包管理系统

呼叫中心线索数据包管理系统，用于管理外呼任务、线索数据包和通话记录分析。

## 📋 项目简介

本系统是一个完整的线索数据包管理解决方案，帮助呼叫中心团队：

- 📦 管理和追踪线索数据包
- 📞 创建和监控外呼任务
- 📊 分析通话数据和标签统计
- 🧮 计算线索需求和成本收益

## 🛠 技术栈

### 前端

- **框架**: React 18
- **构建工具**: Vite 5
- **样式**: Tailwind CSS 3
- **路由**: React Router DOM 6
- **HTTP 客户端**: Axios
- **数据获取**: SWR
- **图表**: Chart.js + react-chartjs-2
- **通知**: React Hot Toast

### 后端

- **框架**: Flask 2.3
- **ORM**: SQLAlchemy 3.0
- **数据库迁移**: Flask-Migrate 4.0
- **开发数据库**: SQLite
- **生产数据库**: PostgreSQL（推荐）

### 部署

- **云服务**: Zeabur（推荐）
- **容器化**: Docker

## 📁 项目结构

```
call-center-lead-management/
├── frontend/                 # 前端项目
│   ├── src/
│   │   ├── components/      # React 组件
│   │   │   └── Header.jsx
│   │   ├── pages/           # 页面组件
│   │   │   ├── Dashboard.jsx
│   │   │   ├── PackageRegister.jsx
│   │   │   ├── PackageDetail.jsx
│   │   │   └── Calculator.jsx
│   │   ├── utils/           # 工具函数
│   │   │   ├── apiClient.js
│   │   │   ├── apiConfig.js
│   │   │   └── tokenManager.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── backend/                  # 后端项目（待创建）
│   ├── app/
│   ├── models/
│   ├── routes/
│   └── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 快速开始

### 前置要求

- Node.js 16+
- Python 3.8+
- npm 或 yarn
- pip

### 安装步骤

#### 1. 克隆仓库

```bash
git clone https://github.com/call-center-org/call-center-lead-management.git
cd call-center-lead-management
```

#### 2. 安装前端依赖

```bash
cd frontend
npm install
```

#### 3. 安装后端依赖

```bash
cd ../backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 4. 初始化数据库

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

#### 5. 启动开发服务器

**后端** (端口 5002):

```bash
cd backend
source venv/bin/activate
python run.py
```

**前端** (端口 3002):

```bash
cd frontend
npm run dev
```

访问 `http://localhost:3002` 查看应用。

## 📊 功能模块

### 1. 首页看板 (Dashboard)

- 关键指标展示（数据包总数、线索总量、接通率、意向率）
- 数据包列表查看
- 快速导航到登记页面

### 2. 数据包登记 (Package Register)

- 数据包基本信息录入
- 数据来源、行业、地区分类
- 线索数量和预期指标设置

### 3. 数据包详情 (Package Detail)

- 数据包完整信息展示
- 外呼任务列表
- 标签统计分析

### 4. 线索需求计算器 (Calculator)

- 基于接通率和意向率计算所需线索量
- 成本收益分析
- ROI 计算

## 🔐 认证机制

系统使用 JWT (JSON Web Token) 进行身份认证：

- Token 存储在 localStorage
- 自动在请求头中添加 Authorization
- Token 过期自动清除并跳转登录

## 🌐 API 端点

### 数据包相关

- `GET /api/packages` - 获取所有数据包
- `POST /api/packages` - 创建数据包
- `GET /api/packages/:id` - 获取单个数据包
- `PUT /api/packages/:id` - 更新数据包
- `DELETE /api/packages/:id` - 删除数据包

### 外呼任务相关

- `POST /api/packages/:id/tasks` - 创建外呼任务
- `GET /api/packages/:id/tasks` - 获取数据包的所有任务

### 指标相关

- `GET /api/metrics` - 获取系统指标
- `GET /api/dashboard` - 获取仪表盘数据

## 🎨 自定义配置

### 修改端口

**前端** - 编辑 `frontend/vite.config.js`:

```javascript
server: {
  port: 3002, // 修改为其他端口
}
```

**后端** - 编辑 `backend/run.py`:

```python
app.run(port=5002)  # 修改为其他端口
```

### 修改主题颜色

编辑 `frontend/tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: '#1E40AF',    // 主色调
      secondary: '#9333EA',  // 次要色
      success: '#10B981',    // 成功色
      danger: '#EF4444',     // 危险色
      warning: '#F59E0B',    // 警告色
    },
  },
}
```

## 📦 部署

### 部署到 Zeabur（推荐）

Zeabur 是一个现代化的云部署平台，支持自动构建和部署。

**快速部署步骤：**

1. 访问 [Zeabur Dashboard](https://dash.zeabur.com)
2. 使用 GitHub 账号登录
3. 创建新项目
4. 从 GitHub 导入此仓库
5. Zeabur 会自动识别前后端服务并部署

**详细部署文档请参考：** `ZEABUR_DEPLOY.md`

**Web 控制台：** https://dash.zeabur.com

**CLI 部署：**
```bash
# 安装 Zeabur CLI
npm install -g @zeabur/cli

# 登录
zeabur auth login

# 部署
zeabur deploy
```

## ⚠️ 开发必读

> **🚨 重要提醒：所有开发人员（包括 AI）必须阅读并严格遵循以下规则**

### 📋 核心原则

1. **唯一的需求来源**
   - ✅ [`docs/PRD.md`](./docs/PRD.md) 是唯一的产品需求文档
   - ✅ 所有功能必须以 PRD 为准，不得擅自修改需求
   - ❌ 不要根据猜测或假设进行开发

2. **唯一的里程碑划分**
   - ✅ 使用 **M0-M4** 里程碑（来自 PRD）
   - ❌ 不要使用 Phase、Sprint 或其他划分方式
   - ✅ 当前阶段：**M0 已完成，M1 进行中**

3. **唯一的进度跟踪文档**
   - ✅ [`docs/MILESTONE_TRACKING.md`](./docs/MILESTONE_TRACKING.md) 是唯一的进度跟踪文档
   - ✅ 完成任务后必须立即更新此文档（将 `[ ]` 改为 `[x]`）
   - ✅ 定期更新进度百分比

### 🎯 开发流程（必须遵守）

**开发前：**
1. 📖 阅读 [`docs/PRD.md`](./docs/PRD.md) 确认需求
2. 📋 查看 [`docs/MILESTONE_TRACKING.md`](./docs/MILESTONE_TRACKING.md) 了解当前任务
3. 🔍 检查验收标准

**开发中：**
1. 🚫 不要偏离 PRD 定义的需求
2. 🚫 不要跳过 M1 直接开发 M2/M3/M4 的功能
3. ✅ 有疑问立即查阅 PRD 和 MILESTONE_TRACKING

**开发后：**
1. ✅ 更新 [`docs/MILESTONE_TRACKING.md`](./docs/MILESTONE_TRACKING.md)
2. ✅ 标记已完成的任务 `[x]`
3. ✅ 更新进度百分比
4. ✅ 提交 Git 时引用任务编号

### 📅 文档更新频率

| 阶段 | 更新频率 | 说明 |
|------|---------|------|
| M1 | 每 2 天 | 任务较多，需密切跟踪 |
| M2-M4 | 每周 | 每周五更新进度 |

### 🤖 AI 协作规则

如果你是 AI（Cursor/Claude 等）：
1. **每次对话开始时**，必须先阅读 `docs/MILESTONE_TRACKING.md` 了解当前进度
2. **做任何开发决策前**，必须先参考 `docs/PRD.md` 确认需求
3. **完成任务后**，必须更新 `docs/MILESTONE_TRACKING.md`
4. **不要**根据记忆或猜测，**一切以文档为准**

### 📂 关键文件位置

```
call-center-lead-management/
├── docs/
│   ├── PRD.md                    ← 📖 产品需求（必读）
│   └── MILESTONE_TRACKING.md     ← 📊 进度跟踪（必读，频繁更新）
├── README.md                     ← 📚 项目入口（当前文件）
└── ...
```

---

## 📚 项目文档

完整的项目文档位于 `docs/` 目录：

- **[PRD - 产品需求文档](./docs/PRD.md)** - 完整的产品需求定义
  - 产品背景与目标
  - 4 个核心页面详细需求
  - 16 个标签规则
  - 业务规则与计算公式
  - 数据库表设计

- **[MILESTONE_TRACKING - 里程碑跟踪](./docs/MILESTONE_TRACKING.md)** - 开发进度监控
  - M0-M4 完整规划
  - 当前进度：M0 ✅ 已完成，M1 🔄 进行中
  - 详细任务清单（33 个任务）
  - 验收标准
  - 时间规划

- **[ZEABUR_DEPLOY - 部署指南](./ZEABUR_DEPLOY.md)** - Zeabur 部署说明

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📝 里程碑进度

当前阶段：**M1 - Cursor 骨架**（0%）

- [x] M0：Figma 低保真（已完成）
- [ ] M1：Cursor 骨架（进行中）
  - [ ] 前端项目搭建
  - [ ] 后端项目搭建
  - [ ] 4 个页面骨架
  - [ ] 基础 API 接口
- [ ] M2：任务逻辑
- [ ] M3：计算器
- [ ] M4：报表与告警

详细进度请查看：[MILESTONE_TRACKING.md](./docs/MILESTONE_TRACKING.md)

## 📄 许可证

MIT License

## 👥 团队

江苏职场呼叫中心团队

---

**当前版本**: v0.1.0 (MVP 开发中)
