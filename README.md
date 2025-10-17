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

- **云服务**: 腾讯云 CloudBase
- **CI/CD**: GitHub Actions
- **容器化**: Docker（可选）

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

### 部署到腾讯云 CloudBase

1. 安装 CloudBase CLI:

```bash
npm install -g @cloudbase/cli
```

2. 登录:

```bash
tcb login
```

3. 部署:

```bash
tcb framework deploy
```

详细部署文档请参考 `docs/deployment.md`（待创建）。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📝 待办事项

- [x] 前端项目初始化
- [x] 基础组件开发
- [ ] 后端 API 开发
- [ ] 数据库表结构创建
- [ ] CloudBase 部署配置
- [ ] 单元测试编写
- [ ] API 文档完善

## 📄 许可证

MIT License

## 👥 团队

江苏职场呼叫中心团队

---

**当前版本**: v0.1.0 (MVP 开发中)
