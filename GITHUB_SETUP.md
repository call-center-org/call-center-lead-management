# GitHub 仓库设置指南

本文档介绍如何将项目推送到 GitHub 仓库。

## 方法一：使用 GitHub CLI（推荐）

### 1. 安装 GitHub CLI

**macOS:**

```bash
brew install gh
```

**其他系统:** 访问 https://cli.github.com/

### 2. 登录 GitHub

```bash
gh auth login
```

按照提示完成登录。

### 3. 运行自动化脚本

```bash
./setup-github-repo.sh
```

脚本会自动：

- 创建 GitHub 仓库（个人或组织）
- 添加远程仓库地址
- 推送代码到 main 分支
- 打开浏览器查看仓库

---

## 方法二：手动创建（传统方式）

### 1. 在 GitHub 网站创建仓库

1. 访问 https://github.com/new
2. 如果要创建到组织：
   - 点击左上角的组织名称下拉菜单
   - 选择 `call-center-org` 组织
3. 填写仓库信息：
   - **Repository name**: `call-center-lead-management`
   - **Description**: 呼叫中心线索数据包管理系统 - 管理外呼任务、线索数据和通话记录分析
   - **Visibility**: Public（公开）或 Private（私有）
   - **不要** 勾选 "Initialize this repository with a README"（我们已有 README）
4. 点击 "Create repository"

### 2. 添加远程仓库并推送

**如果创建到组织:**

```bash
cd /Users/tomnice/call-center-lead-management
git remote add origin https://github.com/call-center-org/call-center-lead-management.git
git branch -M main
git push -u origin main
```

**如果创建到个人账户:**

```bash
cd /Users/tomnice/call-center-lead-management
git remote add origin https://github.com/YOUR_USERNAME/call-center-lead-management.git
git branch -M main
git push -u origin main
```

> 将 `YOUR_USERNAME` 替换为您的 GitHub 用户名

### 3. 验证推送成功

访问仓库地址查看代码：

- 组织: https://github.com/call-center-org/call-center-lead-management
- 个人: https://github.com/YOUR_USERNAME/call-center-lead-management

---

## 后续操作

### 1. 保护 main 分支

**Settings** → **Branches** → **Add branch protection rule**:

- Branch name pattern: `main`
- ✅ Require a pull request before merging
- ✅ Require status checks to pass before merging

### 2. 添加协作者

**Settings** → **Collaborators** → **Add people**

输入 GitHub 用户名或邮箱邀请团队成员。

---

## 常见问题

### Q: 推送时提示 "Permission denied"

**A:** 检查 SSH 密钥是否已添加到 GitHub：

```bash
ssh -T git@github.com
```

如果失败，参考: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

### Q: 推送时提示 "remote: Repository not found"

**A:** 检查：

1. 仓库名称是否正确
2. 是否有权限访问该仓库
3. 如果是组织仓库，确认您是组织成员

### Q: 想要修改远程仓库地址

**A:**

```bash
git remote set-url origin NEW_URL
git remote -v  # 验证修改成功
```

---

## 相关资源

- [GitHub CLI 文档](https://cli.github.com/manual/)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Git 基础教程](https://git-scm.com/book/zh/v2)
