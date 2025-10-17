#!/bin/bash

# 线索数据包管理系统 - GitHub 仓库设置脚本
# 使用 GitHub CLI 创建仓库并推送代码

echo "🚀 开始设置 GitHub 仓库..."

# 检查是否安装了 GitHub CLI
if ! command -v gh &> /dev/null
then
    echo "❌ 未检测到 GitHub CLI (gh)"
    echo "请先安装 GitHub CLI: brew install gh"
    echo "或访问: https://cli.github.com/"
    exit 1
fi

# 检查是否已登录
if ! gh auth status &> /dev/null
then
    echo "📝 请先登录 GitHub..."
    gh auth login
fi

# 仓库信息
REPO_NAME="call-center-lead-management"
ORG_NAME="call-center-org"  # 如果要创建到组织，修改此处
DESCRIPTION="呼叫中心线索数据包管理系统 - 管理外呼任务、线索数据和通话记录分析"

echo ""
echo "📦 仓库信息:"
echo "   名称: $REPO_NAME"
echo "   组织: $ORG_NAME"
echo "   描述: $DESCRIPTION"
echo ""

# 询问用户是否创建到组织还是个人账户
read -p "是否创建到组织 $ORG_NAME? (y/n): " choice
if [[ $choice == "y" || $choice == "Y" ]]; then
    echo "📂 创建组织仓库: $ORG_NAME/$REPO_NAME"
    gh repo create $ORG_NAME/$REPO_NAME --public --description "$DESCRIPTION" --source=. --remote=origin --push
else
    echo "📂 创建个人仓库: $REPO_NAME"
    gh repo create $REPO_NAME --public --description "$DESCRIPTION" --source=. --remote=origin --push
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ GitHub 仓库创建成功！"
    echo ""
    echo "🌐 仓库地址:"
    gh repo view --web
    echo ""
    echo "📝 后续操作:"
    echo "   1. 配置 GitHub Secrets (用于 CloudBase 部署)"
    echo "   2. 开发后端 API"
    echo "   3. 配置 CI/CD 流程"
else
    echo ""
    echo "❌ 仓库创建失败"
    echo "您也可以手动创建仓库，然后运行:"
    echo "   git remote add origin https://github.com/$ORG_NAME/$REPO_NAME.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
fi

