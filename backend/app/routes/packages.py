"""
数据包相关 API 路由
"""

from flask import Blueprint, request, jsonify
from app import db
from app.models import LeadPackage, DialTask

packages_bp = Blueprint("packages", __name__)


@packages_bp.route("", methods=["GET"])
def get_packages():
    """
    获取所有数据包

    查询参数:
        - page: 页码 (默认 1)
        - per_page: 每页数量 (默认 20)
        - source: 数据来源过滤
        - industry: 行业过滤
        - region: 地区过滤
    """
    # 获取查询参数
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    source = request.args.get("source", type=str)
    industry = request.args.get("industry", type=str)
    region = request.args.get("region", type=str)

    # 构建查询
    query = LeadPackage.query

    # 应用过滤
    if source:
        query = query.filter(LeadPackage.source == source)
    if industry:
        query = query.filter(LeadPackage.industry == industry)
    if region:
        query = query.filter(LeadPackage.region == region)

    # 排序：最新的在前
    query = query.order_by(LeadPackage.created_at.desc())

    # 分页
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify(
        {
            "success": True,
            "data": [package.to_dict() for package in pagination.items],
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": pagination.total,
                "pages": pagination.pages,
            },
        }
    )


@packages_bp.route("", methods=["POST"])
def create_package():
    """
    创建数据包

    请求体:
        {
            "name": "数据包名称",
            "source": "数据来源",
            "industry": "所属行业",
            "region": "所属地区",
            "total_leads": 1000,
            "valid_leads": 900,
            "cost_per_lead": 2.5
        }
    """
    data = request.get_json()

    # 验证必填字段
    if not data.get("name") or not data.get("source"):
        return jsonify({"success": False, "error": "缺少必填字段: name, source"}), 400

    # 创建数据包
    package = LeadPackage(
        name=data["name"],
        source=data["source"],
        industry=data.get("industry"),
        region=data.get("region"),
        total_leads=data.get("total_leads", 0),
        valid_leads=data.get("valid_leads", 0),
        cost_per_lead=data.get("cost_per_lead", 0.0),
    )

    # 计算指标
    package.calculate_metrics()

    # 保存到数据库
    db.session.add(package)
    db.session.commit()

    return (
        jsonify(
            {"success": True, "data": package.to_dict(), "message": "数据包创建成功"}
        ),
        201,
    )


@packages_bp.route("/<int:package_id>", methods=["GET"])
def get_package(package_id):
    """获取单个数据包详情"""
    package = LeadPackage.query.get_or_404(package_id)

    # 获取关联的外呼任务
    tasks = [task.to_dict() for task in package.dial_tasks.all()]

    # 获取标签汇总
    tag_summaries = [summary.to_dict() for summary in package.tag_summaries.all()]

    result = package.to_dict()
    result["dial_tasks"] = tasks
    result["tag_summaries"] = tag_summaries

    return jsonify({"success": True, "data": result})


@packages_bp.route("/<int:package_id>", methods=["PUT"])
def update_package(package_id):
    """
    更新数据包

    请求体:
        {
            "name": "新名称",
            "total_leads": 1200,
            ...
        }
    """
    package = LeadPackage.query.get_or_404(package_id)
    data = request.get_json()

    # 更新字段
    allowed_fields = [
        "name",
        "source",
        "industry",
        "region",
        "total_leads",
        "valid_leads",
        "contact_rate",
        "interest_rate",
        "cost_per_lead",
    ]

    for field in allowed_fields:
        if field in data:
            setattr(package, field, data[field])

    # 重新计算指标
    package.calculate_metrics()

    db.session.commit()

    return jsonify(
        {"success": True, "data": package.to_dict(), "message": "数据包更新成功"}
    )


@packages_bp.route("/<int:package_id>", methods=["DELETE"])
def delete_package(package_id):
    """删除数据包"""
    package = LeadPackage.query.get_or_404(package_id)

    db.session.delete(package)
    db.session.commit()

    return jsonify({"success": True, "message": "数据包删除成功"})


@packages_bp.route("/<int:package_id>/tasks", methods=["GET"])
def get_package_tasks(package_id):
    """获取数据包的所有外呼任务"""
    package = LeadPackage.query.get_or_404(package_id)

    tasks = [task.to_dict() for task in package.dial_tasks.all()]

    return jsonify({"success": True, "data": tasks})


@packages_bp.route("/<int:package_id>/tasks", methods=["POST"])
def create_package_task(package_id):
    """
    为数据包创建外呼任务

    请求体:
        {
            "task_name": "任务名称",
            "description": "任务描述",
            "start_time": "2025-10-18T09:00:00",
            "end_time": "2025-10-18T18:00:00"
        }
    """
    package = LeadPackage.query.get_or_404(package_id)
    data = request.get_json()

    if not data.get("task_name"):
        return jsonify({"success": False, "error": "缺少必填字段: task_name"}), 400

    from app.models import DialTask
    from datetime import datetime

    # 创建外呼任务
    task = DialTask(
        package_id=package_id,
        task_name=data["task_name"],
        description=data.get("description"),
        start_time=(
            datetime.fromisoformat(data["start_time"])
            if data.get("start_time")
            else None
        ),
        end_time=(
            datetime.fromisoformat(data["end_time"]) if data.get("end_time") else None
        ),
    )

    db.session.add(task)
    db.session.commit()

    return (
        jsonify(
            {"success": True, "data": task.to_dict(), "message": "外呼任务创建成功"}
        ),
        201,
    )
