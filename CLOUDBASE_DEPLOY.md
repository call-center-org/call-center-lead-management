# CloudBase 部署指南

本文档描述如何将线索管理系统部署到腾讯云CloudBase。

## 前置要求

1. **腾讯云账号**
   - 已开通CloudBase服务
   - 创建CloudBase环境

2. **本地工具**
   ```bash
   # 安装CloudBase CLI
   npm install -g @cloudbase/cli
   
   # 登录CloudBase
   cloudbase login
   ```

## 部署步骤

### 1. 配置环境变量

在CloudBase控制台中配置以下环境变量：

```bash
# 数据库连接（使用CloudBase PostgreSQL或自建）
DATABASE_URL=postgresql://user:password@host:5432/dbname

# 应用密钥（务必使用强密码）
SECRET_KEY=your-super-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production

# 环境配置
FLASK_ENV=production
```

### 2. 修改cloudbaserc.json

将`cloudbaserc.json`中的占位符替换为实际值：

```json
{
  "envId": "your-cloudbase-env-id",  // 替换为你的环境ID
  ...
}
```

### 3. 部署前端

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 构建生产版本
npm run build

# 部署到CloudBase
cloudbase framework deploy -e your-env-id
```

### 4. 部署后端

```bash
# 返回项目根目录
cd ..

# 部署后端容器
cloudbase framework deploy -e your-env-id
```

## 数据库迁移

### 首次部署

部署后需要初始化数据库：

```bash
# 进入后端容器
cloudbase run exec lead-management-api -e your-env-id

# 运行数据库迁移
flask db upgrade
```

### 创建管理员用户

```bash
# 在容器中执行Python脚本
python -c "
from app import create_app, db
from app.models import User

app = create_app('production')
with app.app_context():
    admin = User.create_user(
        username='admin',
        email='admin@example.com',
        password='change-this-password',
        full_name='系统管理员',
        role='admin'
    )
    db.session.add(admin)
    db.session.commit()
    print('管理员用户创建成功')
"
```

## 环境配置说明

### 开发环境（Development）
- 数据库：SQLite
- 端口：
  - 前端：3002
  - 后端：5002

### 生产环境（Production/CloudBase）
- 数据库：PostgreSQL (推荐CloudBase PostgreSQL)
- 容器：Gunicorn + Flask
- 前端：静态网站托管

## CloudBase架构

```
┌─────────────────┐
│   CloudBase     │
│   静态网站托管   │  (前端)
│   /             │
└────────┬────────┘
         │
         │  API请求 (/api/*)
         │
         ▼
┌─────────────────┐
│   CloudBase     │
│   容器服务      │  (后端)
│   Flask + Gunicorn
└────────┬────────┘
         │
         │  数据库连接
         │
         ▼
┌─────────────────┐
│   PostgreSQL    │
│   CloudBase DB  │
└─────────────────┘
```

## 常见问题

### Q1: 数据库连接失败
**A**: 检查`DATABASE_URL`环境变量格式是否正确，确保数据库实例可访问。

### Q2: 容器启动失败
**A**: 查看CloudBase控制台日志，检查：
- 环境变量是否配置完整
- Docker镜像是否构建成功
- 端口配置是否正确

### Q3: API请求404
**A**: 检查：
- cloudbaserc.json中的`servicePath`配置
- 前端API基础URL配置

## 监控和日志

### 查看后端日志
```bash
cloudbase run log lead-management-api -e your-env-id --tail 100
```

### 健康检查
访问：`https://your-env.service.tcloudbase.com/api/metrics/dashboard`

## 回滚

如果部署出现问题，可以回滚到上一版本：

```bash
cloudbase framework rollback -e your-env-id
```

## 性能优化

### 前端
- 已启用Vite生产构建优化
- 已配置代码分割
- 静态资源CDN加速

### 后端
- Gunicorn多进程配置（2 workers, 4 threads）
- 数据库连接池
- API响应缓存（可选）

## 成本估算

基于1000个数据包/月的使用量：
- 静态网站托管：约 ¥5/月
- 容器服务：约 ¥30-50/月
- PostgreSQL数据库：约 ¥50-100/月
- **总计**: 约 ¥85-155/月

## 安全建议

1. ✅ 使用强密钥（SECRET_KEY, JWT_SECRET_KEY）
2. ✅ 启用HTTPS（CloudBase默认支持）
3. ✅ 定期更新依赖包
4. ✅ 设置数据库访问白名单
5. ✅ 启用日志审计

## 参考链接

- [CloudBase官方文档](https://cloud.tencent.com/document/product/876)
- [CloudBase Framework文档](https://cloudbase.net/framework.html)
- [Flask生产部署最佳实践](https://flask.palletsprojects.com/en/2.3.x/deploying/)

