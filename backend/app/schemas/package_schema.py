"""
Lead Package related schemas
"""

from marshmallow import Schema, fields, validate, validates, ValidationError


class LeadPackageSchema(Schema):
    """数据包Schema（完整信息）"""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    source = fields.Str(required=True, validate=validate.Length(max=100))
    industry = fields.Str(required=True, validate=validate.Length(max=100))
    region = fields.Str(required=True, validate=validate.Length(max=100))
    total_leads = fields.Int(required=True, validate=validate.Range(min=0))
    valid_leads = fields.Int(required=True, validate=validate.Range(min=0))
    contact_rate = fields.Float(dump_only=True)
    interest_rate = fields.Float(dump_only=True)
    cost_per_lead = fields.Float(validate=validate.Range(min=0))
    total_cost = fields.Float(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class LeadPackageCreateSchema(Schema):
    """创建数据包Schema"""
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255),
        error_messages={"required": "数据包名称不能为空"}
    )
    source = fields.Str(
        required=True,
        validate=validate.Length(max=100),
        error_messages={"required": "来源不能为空"}
    )
    industry = fields.Str(
        required=True,
        validate=validate.Length(max=100),
        error_messages={"required": "行业/年级不能为空"}
    )
    region = fields.Str(
        required=True,
        validate=validate.Length(max=100),
        error_messages={"required": "区域不能为空"}
    )
    total_leads = fields.Int(
        required=True,
        validate=validate.Range(min=1),
        error_messages={"required": "总线索数不能为空"}
    )
    valid_leads = fields.Int(
        required=True,
        validate=validate.Range(min=1),
        error_messages={"required": "有效线索数不能为空"}
    )
    cost_per_lead = fields.Float(
        validate=validate.Range(min=0),
        missing=1.0  # 默认值1元
    )

    @validates("valid_leads")
    def validate_valid_leads(self, value):
        """验证有效线索数不能超过总线索数"""
        total_leads = self.context.get("total_leads")
        if total_leads and value > total_leads:
            raise ValidationError("有效线索数不能超过总线索数")
        return value


class LeadPackageUpdateSchema(Schema):
    """更新数据包Schema"""
    name = fields.Str(validate=validate.Length(min=1, max=255))
    source = fields.Str(validate=validate.Length(max=100))
    industry = fields.Str(validate=validate.Length(max=100))
    region = fields.Str(validate=validate.Length(max=100))
    total_leads = fields.Int(validate=validate.Range(min=1))
    valid_leads = fields.Int(validate=validate.Range(min=1))
    cost_per_lead = fields.Float(validate=validate.Range(min=0))

