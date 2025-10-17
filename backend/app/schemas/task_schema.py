"""
Dial Task related schemas
"""

from marshmallow import Schema, fields, validate


class DialTaskSchema(Schema):
    """外呼任务Schema（完整信息）"""
    id = fields.Int(dump_only=True)
    package_id = fields.Int(required=True)
    task_name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    description = fields.Str(allow_none=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(allow_none=True)
    status = fields.Str(
        validate=validate.OneOf(["pending", "in_progress", "completed", "failed"]),
        missing="pending"
    )
    total_calls = fields.Int(dump_only=True)
    connected_calls = fields.Int(dump_only=True)
    interested_calls = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class DialTaskCreateSchema(Schema):
    """创建外呼任务Schema"""
    package_id = fields.Int(
        required=True,
        error_messages={"required": "数据包ID不能为空"}
    )
    task_name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255),
        error_messages={"required": "任务名称不能为空"}
    )
    description = fields.Str(allow_none=True)
    start_time = fields.DateTime(
        required=True,
        error_messages={"required": "开始时间不能为空"}
    )
    end_time = fields.DateTime(allow_none=True)
    status = fields.Str(
        validate=validate.OneOf(["pending", "in_progress", "completed", "failed"]),
        missing="pending"
    )


class DialTaskUpdateSchema(Schema):
    """更新外呼任务Schema"""
    task_name = fields.Str(validate=validate.Length(min=1, max=255))
    description = fields.Str(allow_none=True)
    start_time = fields.DateTime()
    end_time = fields.DateTime(allow_none=True)
    status = fields.Str(
        validate=validate.OneOf(["pending", "in_progress", "completed", "failed"])
    )

