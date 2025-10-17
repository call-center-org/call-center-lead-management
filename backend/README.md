# 线索数据包管理系统 - 后端 API

Flask 后端 API 服务，为线索数据包管理系统提供数据接口。

## 📋 技术栈

- **框架**: Flask 2.3
- **ORM**: SQLAlchemy 3.0
- **数据库迁移**: Flask-Migrate 4.0
- **认证**: JWT (Flask-JWT-Extended)
- **开发数据库**: SQLite
- **生产数据库**: PostgreSQL

## 🚀 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 并创建 `.env` 文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置必要的环境变量。

### 3. 初始化数据库

```bash
# 初始化数据库迁移
flask db init

# 创建迁移文件
flask db migrate -m "Initial migration"

# 执行迁移
flask db upgrade

# 或者直接创建表（开发环境）
flask init-db
```

### 4. 启动开发服务器

```bash
python run.py
```

服务器将在 `http://localhost:5002` 启动。

## 📊 数据库模型

### 1. LeadPackage (线索数据包)

存储线索数据包的基本信息和指标。

```python
- id: 主键
- name: 数据包名称
- source: 数据来源
- industry: 所属行业
- region: 所属地区
- total_leads: 线索总数
- valid_leads: 有效线索数
- contact_rate: 接通率
- interest_rate: 意向率
- cost_per_lead: 单条线索成本
- total_cost: 总成本
- created_at, updated_at
```

### 2. DialTask (外呼任务)

管理外呼任务。

```python
- id: 主键
- package_id: 关联数据包
- task_name: 任务名称
- description: 任务描述
- start_time, end_time: 任务时间
- status: 任务状态 (pending/in_progress/completed/cancelled)
- total_calls, connected_calls, interested_calls
- created_at, updated_at
```

### 3. Call (通话记录)

记录每次通话的详细信息。

```python
- id: 主键
- task_id: 关联外呼任务
- phone_number: 电话号码
- call_time: 拨打时间
- duration: 通话时长（秒）
- result: 通话结果 (connected/voicemail/busy/no_answer/rejected)
- notes: 通话备注
- customer_name, company
- created_at, updated_at
```

### 4. CallTag (通话标签)

为通话记录添加标签。

```python
- id: 主键
- call_id: 关联通话记录
- tag_name: 标签名称
- tag_value: 标签值
- tag_type: 标签类型
- created_at
```

### 5. PackageTagSummary (数据包标签汇总)

数据包级别的标签统计。

```python
- id: 主键
- package_id: 关联数据包
- tag_name, tag_value: 标签信息
- tag_count: 标签出现次数
- percentage: 占比
- created_at, updated_at
```

### 6. MetricsSummary (指标汇总)

按日汇总的系统指标。

```python
- id: 主键
- date: 汇总日期
- total_packages, new_packages, total_leads
- total_calls, connected_calls, total_duration
- avg_contact_rate, avg_interest_rate, avg_call_duration
- total_cost, total_revenue, roi
- created_at, updated_at
```

## 🌐 API 端点

### 数据包相关 (`/api/packages`)

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/packages` | 获取所有数据包（支持分页和过滤） |
| POST | `/api/packages` | 创建数据包 |
| GET | `/api/packages/:id` | 获取单个数据包详情 |
| PUT | `/api/packages/:id` | 更新数据包 |
| DELETE | `/api/packages/:id` | 删除数据包 |
| GET | `/api/packages/:id/tasks` | 获取数据包的所有任务 |
| POST | `/api/packages/:id/tasks` | 为数据包创建任务 |

### 外呼任务相关 (`/api/tasks`)

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/tasks/:id` | 获取任务详情 |
| PUT | `/api/tasks/:id` | 更新任务 |
| DELETE | `/api/tasks/:id` | 删除任务 |
| GET | `/api/tasks/:id/calls` | 获取任务的所有通话 |
| POST | `/api/tasks/:id/calls` | 创建通话记录 |
| POST | `/api/tasks/:id/metrics` | 更新任务指标 |

### 指标查询相关 (`/api/metrics`)

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/metrics/dashboard` | 获取仪表盘数据 |
| GET | `/api/metrics/summary` | 获取指标汇总 |
| POST | `/api/metrics/summary/today` | 计算今日指标 |
| GET | `/api/metrics/trends` | 获取趋势数据 |
| GET | `/api/metrics/package/:id/stats` | 获取数据包详细统计 |

## 📝 API 请求示例

### 创建数据包

```bash
curl -X POST http://localhost:5002/api/packages \
  -H "Content-Type: application/json" \
  -d '{
    "name": "测试数据包",
    "source": "线上渠道",
    "industry": "科技",
    "region": "江苏",
    "total_leads": 1000,
    "valid_leads": 900,
    "cost_per_lead": 2.5
  }'
```

### 获取仪表盘数据

```bash
curl http://localhost:5002/api/metrics/dashboard
```

### 创建通话记录

```bash
curl -X POST http://localhost:5002/api/tasks/1/calls \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "13800138000",
    "duration": 120,
    "result": "connected",
    "notes": "客户有意向",
    "tags": [
      {"tag_name": "interest_level", "tag_value": "high"}
    ]
  }'
```

## 🛠 开发命令

### Flask CLI 命令

```bash
# 初始化数据库
flask init-db

# 填充测试数据
flask seed-db

# 数据库迁移
flask db migrate -m "Migration message"
flask db upgrade
flask db downgrade
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行测试并显示覆盖率
pytest --cov=app
```

## 🔐 认证机制

本系统使用 JWT Token 进行身份认证（当前版本未启用，待后续开发）。

## 📦 部署

### 部署到腾讯云 CloudBase

1. 配置环境变量
2. 设置 PostgreSQL 数据库
3. 运行数据库迁移
4. 启动应用

详细部署文档请参考项目根目录的部署指南。

## 🐛 调试

开发环境默认开启 SQL 日志，可以在控制台看到所有 SQL 语句。

如需关闭，修改 `config.py`:

```python
SQLALCHEMY_ECHO = False
```

## 📝 待办事项

- [ ] 添加用户认证和权限管理
- [ ] 实现 JWT Token 认证
- [ ] 添加数据验证（Marshmallow Schema）
- [ ] 完善错误处理
- [ ] 添加单元测试
- [ ] 实现 CSV 导出功能
- [ ] 添加 API 文档（Swagger）
- [ ] 性能优化和缓存

## 📄 许可证

MIT License

