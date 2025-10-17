# Zeabur 部署指南

## 📦 项目已准备就绪

本项目已配置好 Zeabur 部署所需的文件：
- ✅ `zeabur.json` - 主配置文件
- ✅ `backend/zbconfig.json` - 后端配置
- ✅ 前端 API 配置已支持 Zeabur 环境

## 🚀 使用 Zeabur 插件部署

### 方法一：使用 VSCode/Cursor 插件（推荐）

1. **打开命令面板**
   - Mac: `Cmd + Shift + P`
   - Windows/Linux: `Ctrl + Shift + P`

2. **搜索并执行 Zeabur 命令**
   - 输入 `Zeabur: Deploy`
   - 或者 `Zeabur: Create Project`

3. **按照插件提示操作**
   - 选择要部署的服务（backend / frontend）
   - 插件会自动读取 `zeabur.json` 配置
   - 跟随向导完成部署

### 方法二：使用 Zeabur CLI

1. **安装 Zeabur CLI**
   ```bash
   npm install -g @zeabur/cli
   ```

2. **登录 Zeabur**
   ```bash
   zeabur login
   ```

3. **部署项目**
   ```bash
   # 部署整个项目
   zeabur deploy
   
   # 或单独部署服务
   zeabur deploy --service backend
   zeabur deploy --service frontend
   ```

### 方法三：使用 Zeabur 网页控制台

1. 访问 https://dash.zeabur.com
2. 点击 "New Project"
3. 选择 "Import from GitHub"
4. 选择 `call-center-lead-management` 仓库
5. Zeabur 会自动识别配置并部署

## 🔧 环境变量配置

### 后端必需的环境变量

在 Zeabur 控制台或插件中添加：

```
SECRET_KEY=8e359590ab5268b7b7854530fbd96cf96828f699aa08d2bbf8d2f6e373c1b5c8
JWT_SECRET_KEY=b51b16d085809f4e32fc7c0e701f14dd129f241ff839975e50013ed12b80c27c4
```

### 前端环境变量（部署后端后添加）

```
VITE_API_URL=https://你的后端域名.zeabur.app/api
```

## 📝 部署后的配置步骤

1. **获取后端域名**
   - 后端部署完成后，在 Zeabur 控制台找到后端服务
   - 复制自动生成的域名（如：`backend-xxx.zeabur.app`）

2. **更新前端环境变量**
   - 在前端服务的环境变量中添加：
   ```
   VITE_API_URL=https://backend-xxx.zeabur.app/api
   ```
   - 保存后前端会自动重新部署

3. **访问你的应用**
   - 前端地址：`https://frontend-xxx.zeabur.app`
   - 后端 API：`https://backend-xxx.zeabur.app/api`

## 🎯 快速开始

### 如果使用插件：

1. 确保已在 VSCode/Cursor 中安装 Zeabur 插件
2. 打开命令面板（`Cmd/Ctrl + Shift + P`）
3. 输入 `Zeabur` 查看可用命令
4. 选择 `Zeabur: Deploy` 开始部署

### 常用插件命令：

- `Zeabur: Deploy` - 部署项目
- `Zeabur: View Logs` - 查看部署日志
- `Zeabur: Open Dashboard` - 打开 Web 控制台
- `Zeabur: Add Environment Variable` - 添加环境变量

## 💡 注意事项

1. **首次部署**：建议先部署后端，获取域名后再部署前端
2. **数据持久化**：目前使用 SQLite，数据保存在容器中。如需持久化，建议添加 Zeabur 的 PostgreSQL 服务
3. **自定义域名**：可在 Zeabur 控制台绑定自己的域名
4. **免费额度**：Zeabur 提供免费套餐，适合测试和小型项目

## 🔗 相关链接

- Zeabur 官网：https://zeabur.com
- Zeabur 文档：https://zeabur.com/docs
- Zeabur Dashboard：https://dash.zeabur.com

## ❓ 常见问题

### Q: 前端无法连接后端？
A: 检查前端的 `VITE_API_URL` 环境变量是否正确设置为后端域名

### Q: 如何查看部署日志？
A: 
- 插件：命令面板 → `Zeabur: View Logs`
- 网页：在 Dashboard 中点击服务 → Logs 标签

### Q: 如何回滚到之前的版本？
A: 在 Zeabur Dashboard 的 Deployments 标签中选择历史版本进行回滚

## 🎉 部署完成！

部署成功后，你将获得：
- ✅ 自动 HTTPS 证书
- ✅ 全球 CDN 加速
- ✅ 自动容器化部署
- ✅ 实时日志查看
- ✅ 一键回滚功能

