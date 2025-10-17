"""
User related schemas
"""

from marshmallow import Schema, fields, validate, validates, ValidationError


class UserSchema(Schema):
    """用户信息Schema"""
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    full_name = fields.Str(allow_none=True, validate=validate.Length(max=120))
    role = fields.Str(dump_only=True)
    is_active = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    last_login = fields.DateTime(dump_only=True)


class UserRegistrationSchema(Schema):
    """用户注册Schema"""
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=80),
        error_messages={"required": "用户名不能为空"}
    )
    email = fields.Email(
        required=True,
        error_messages={"required": "邮箱不能为空", "invalid": "邮箱格式不正确"}
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=6, max=128),
        error_messages={"required": "密码不能为空"}
    )
    full_name = fields.Str(
        allow_none=True,
        validate=validate.Length(max=120)
    )

    @validates("password")
    def validate_password(self, value):
        """验证密码强度"""
        if len(value) < 6:
            raise ValidationError("密码长度至少6位")
        # 可以添加更多密码强度验证规则
        return value


class UserLoginSchema(Schema):
    """用户登录Schema"""
    username = fields.Str(
        required=True,
        error_messages={"required": "用户名/邮箱不能为空"}
    )
    password = fields.Str(
        required=True,
        error_messages={"required": "密码不能为空"}
    )


class UserUpdateSchema(Schema):
    """用户信息更新Schema"""
    email = fields.Email(error_messages={"invalid": "邮箱格式不正确"})
    full_name = fields.Str(validate=validate.Length(max=120))


class ChangePasswordSchema(Schema):
    """修改密码Schema"""
    old_password = fields.Str(
        required=True,
        error_messages={"required": "旧密码不能为空"}
    )
    new_password = fields.Str(
        required=True,
        validate=validate.Length(min=6, max=128),
        error_messages={"required": "新密码不能为空"}
    )

