# GitHub Actions 自动部署到 CloudBase

本项目已配置 GitHub Actions，可以在每次推送代码到 `main` 分支时自动部署前后端到腾讯云 CloudBase。

## 🚀 快速开始

### 1. 获取腾讯云 API 密钥

1. 访问腾讯云控制台：https://console.cloud.tencent.com/cam/capi
2. 点击"新建密钥"
3. 获取以下信息：
   - **SecretId**（例如：AKIDxxxxxxxxxxxx）
   - **SecretKey**（例如：xxxxxxxxxxxxxxxx）

### 2. 配置 GitHub Secrets

1. 打开 GitHub 仓库页面
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**，添加以下两个密钥：

   **密钥 1：**
   - Name: `CLOUDBASE_SECRET_ID`
   - Value: 你的腾讯云 SecretId

   **密钥 2：**
   - Name: `CLOUDBASE_SECRET_KEY`
   - Value: 你的腾讯云 SecretKey

### 3. 触发部署

配置完成后，有两种方式触发部署：

**方式 1：自动触发**
```bash
git add .
git commit -m "feat: 添加新功能"
git push origin main
```
推送代码到 `main` 分支会自动触发部署。

**方式 2：手动触发**
1. 在 GitHub 仓库页面
2. 点击 **Actions** 标签
3. 选择 **Deploy to CloudBase** workflow
4. 点击 **Run workflow** 按钮

## 📋 部署流程

GitHub Actions 会自动执行以下步骤：

1. ✅ 检出代码
2. ✅ 设置 Node.js 环境
3. ✅ 安装 CloudBase CLI
4. ✅ 使用 API 密钥登录 CloudBase
5. ✅ 部署前端到静态网站托管
6. ✅ 部署后端到云托管（容器服务）
7. ✅ 显示部署结果

整个过程大约需要 **5-10 分钟**。

## 🔍 查看部署状态

1. 在 GitHub 仓库点击 **Actions** 标签
2. 查看最新的 workflow 运行记录
3. 点击查看详细日志

## 📦 部署产物

**前端地址：**
https://cloud1-6gt5ulxm10210d0f-1300255017.tcloudbaseapp.com/lead-management

**后端 API 地址：**
https://lead-management-api-193614-4-1300255017.sh.run.tcloudbase.com/api/

## ⚙️ 配置文件

- `.github/workflows/deploy.yml` - GitHub Actions 工作流配置
- `cloudbaserc.json` - CloudBase 部署配置
- `backend/Dockerfile` - 后端容器镜像配置

## 🛠️ 故障排查

### 问题 1：部署失败 - 认证错误
**原因**：GitHub Secrets 未配置或配置错误

**解决**：
1. 检查 Secrets 名称是否正确（区分大小写）
2. 确认 SecretId 和 SecretKey 是否正确
3. 确认 API 密钥有 CloudBase 的操作权限

### 问题 2：部署超时
**原因**：网络问题或构建时间过长

**解决**：
1. 重新运行 workflow
2. 检查 CloudBase 服务状态

### 问题 3：前端部署成功，后端失败
**原因**：云托管配置或 Dockerfile 问题

**解决**：
1. 检查 `backend/Dockerfile` 是否正确
2. 查看 CloudBase 控制台的云托管日志
3. 确认环境变量已在 `cloudbaserc.json` 中配置

## 📝 注意事项

1. **首次部署**可能需要较长时间（5-10分钟）
2. **后续部署**会更快（2-5分钟）
3. **环境变量**已在 `cloudbaserc.json` 中配置，无需在 GitHub Secrets 中重复配置
4. **数据库**使用 SQLite，存储在容器内部，重启会丢失数据
5. 如需持久化数据，建议配置 CloudBase PostgreSQL 数据库

## 🎯 最佳实践

1. **分支保护**：建议为 `main` 分支设置保护规则，要求 PR 审核后才能合并
2. **环境分离**：可以配置 `dev` 分支部署到测试环境
3. **回滚机制**：如果新版本有问题，可以回退 commit 并重新部署
4. **监控告警**：配置 CloudBase 的监控和告警，及时发现问题

## 📚 相关文档

- [CloudBase CLI 文档](https://docs.cloudbase.net/cli-v1/intro.html)
- [CloudBase Framework 文档](https://docs.cloudbase.net/framework/)
- [GitHub Actions 文档](https://docs.github.com/cn/actions)

