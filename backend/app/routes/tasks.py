"""
外呼任务相关 API 路由
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models import DialTask, Call, CallTag

tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.route("/<int:task_id>", methods=["GET"])
def get_task(task_id):
    """获取外呼任务详情"""
    task = DialTask.query.get_or_404(task_id)

    # 获取通话记录
    calls = [call.to_dict() for call in task.calls.all()]

    result = task.to_dict()
    result["calls"] = calls

    return jsonify({"success": True, "data": result})


@tasks_bp.route("/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """
    更新外呼任务

    请求体:
        {
            "task_name": "新任务名称",
            "status": "in_progress",
            "start_time": "2025-10-18T09:00:00"
        }
    """
    task = DialTask.query.get_or_404(task_id)
    data = request.get_json()

    # 更新字段
    allowed_fields = ["task_name", "description", "status"]

    for field in allowed_fields:
        if field in data:
            setattr(task, field, data[field])

    # 更新时间字段
    if "start_time" in data:
        task.start_time = datetime.fromisoformat(data["start_time"])
    if "end_time" in data:
        task.end_time = datetime.fromisoformat(data["end_time"])

    db.session.commit()

    return jsonify({"success": True, "data": task.to_dict(), "message": "任务更新成功"})


@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """删除外呼任务"""
    task = DialTask.query.get_or_404(task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"success": True, "message": "任务删除成功"})


@tasks_bp.route("/<int:task_id>/calls", methods=["GET"])
def get_task_calls(task_id):
    """获取任务的所有通话记录"""
    task = DialTask.query.get_or_404(task_id)

    # 获取查询参数
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 50, type=int)
    result_filter = request.args.get("result", type=str)

    # 构建查询
    query = task.calls

    # 应用过滤
    if result_filter:
        query = query.filter(Call.result == result_filter)

    # 排序：最新的在前
    query = query.order_by(Call.call_time.desc())

    # 分页
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify(
        {
            "success": True,
            "data": [call.to_dict() for call in pagination.items],
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": pagination.total,
                "pages": pagination.pages,
            },
        }
    )


@tasks_bp.route("/<int:task_id>/calls", methods=["POST"])
def create_call(task_id):
    """
    创建通话记录

    请求体:
        {
            "phone_number": "13800138000",
            "call_time": "2025-10-18T10:30:00",
            "duration": 120,
            "result": "connected",
            "notes": "客户有意向",
            "customer_name": "张三",
            "company": "ABC公司",
            "tags": [
                {"tag_name": "interest_level", "tag_value": "high"},
                {"tag_name": "industry", "tag_value": "科技"}
            ]
        }
    """
    task = DialTask.query.get_or_404(task_id)
    data = request.get_json()

    if not data.get("phone_number"):
        return jsonify({"success": False, "error": "缺少必填字段: phone_number"}), 400

    # 创建通话记录
    call = Call(
        task_id=task_id,
        phone_number=data["phone_number"],
        call_time=(
            datetime.fromisoformat(data["call_time"])
            if data.get("call_time")
            else datetime.utcnow()
        ),
        duration=data.get("duration", 0),
        result=data.get("result", "no_answer"),
        notes=data.get("notes"),
        customer_name=data.get("customer_name"),
        company=data.get("company"),
    )

    db.session.add(call)
    db.session.flush()  # 获取 call.id

    # 添加标签
    if data.get("tags"):
        for tag_data in data["tags"]:
            tag = CallTag(
                call_id=call.id,
                tag_name=tag_data["tag_name"],
                tag_value=tag_data.get("tag_value"),
                tag_type=tag_data.get("tag_type", "custom"),
            )
            db.session.add(tag)

    db.session.commit()

    # 更新任务指标
    task.calculate_metrics()
    db.session.commit()

    return (
        jsonify(
            {"success": True, "data": call.to_dict(), "message": "通话记录创建成功"}
        ),
        201,
    )


@tasks_bp.route("/<int:task_id>/metrics", methods=["POST"])
def update_task_metrics(task_id):
    """手动触发任务指标更新"""
    task = DialTask.query.get_or_404(task_id)

    task.calculate_metrics()
    db.session.commit()

    return jsonify({"success": True, "data": task.to_dict(), "message": "指标更新成功"})
