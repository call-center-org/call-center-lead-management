# 线索数据包管理系统 - 快速启动指南

## 📦 项目简介

呼叫中心线索数据包管理系统，包含前端和后端两部分。

## 🚀 快速启动

### 1. 启动后端 API（端口 5002）

```bash
# 进入后端目录
cd backend

# 激活虚拟环境
source venv/bin/activate

# 启动服务器
python run.py
```

后端将在 `http://localhost:5002` 启动。

### 2. 启动前端（端口 3002）

```bash
# 打开新终端，进入前端目录
cd frontend

# 安装依赖（首次运行）
npm install

# 启动开发服务器
npm run dev
```

前端将在 `http://localhost:3002` 启动。

## 📊 已有测试数据

后端已包含测试数据：
- 1 个数据包（1000条线索）
- 1 个外呼任务（5条通话记录）
- 接通率：60%

## 🌐 API 端点

### 数据包相关
- `GET /api/packages` - 获取所有数据包
- `POST /api/packages` - 创建数据包
- `GET /api/packages/:id` - 获取数据包详情
- `PUT /api/packages/:id` - 更新数据包
- `DELETE /api/packages/:id` - 删除数据包

### 外呼任务相关
- `GET /api/tasks/:id` - 获取任务详情
- `GET /api/tasks/:id/calls` - 获取任务的通话记录
- `POST /api/tasks/:id/calls` - 创建通话记录

### 指标相关
- `GET /api/metrics/dashboard` - 获取仪表盘数据
- `GET /api/metrics/summary` - 获取指标汇总
- `GET /api/metrics/trends` - 获取趋势数据

## 📝 测试 API

```bash
cd backend
source venv/bin/activate
python test_api.py
```

## 🛠 技术栈

### 前端
- React 18 + Vite 5
- Tailwind CSS 3
- Axios + SWR
- React Router DOM 6

### 后端
- Flask 2.3
- SQLAlchemy 3.0
- SQLite (开发环境)
- Flask-Migrate 4.0

## 📁 项目结构

```
call-center-lead-management/
├── frontend/                 # 前端项目
│   ├── src/
│   │   ├── components/      # React 组件
│   │   ├── pages/           # 页面组件
│   │   ├── utils/           # 工具函数
│   │   └── App.jsx
│   └── package.json
├── backend/                  # 后端项目
│   ├── app/
│   │   ├── models/          # 数据库模型
│   │   └── routes/          # API 路由
│   ├── migrations/          # 数据库迁移
│   ├── run.py               # 启动文件
│   └── requirements.txt
└── README.md
```

## 🎯 主要功能

1. **数据包管理** - 登记和管理线索数据包
2. **外呼任务** - 创建和追踪外呼任务
3. **通话记录** - 记录每次通话的详细信息
4. **数据统计** - 查看关键指标和趋势分析
5. **需求计算器** - 计算所需线索量和成本收益

## 📞 联系方式

项目问题请在 GitHub Issues 中提交。

---

**当前版本**: v0.1.0 (MVP)  
**最后更新**: 2025-10-17

