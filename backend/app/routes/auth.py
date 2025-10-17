"""
用户认证相关 API 路由
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from marshmallow import ValidationError
from datetime import datetime
from app import db
from app.models import User
from app.schemas import (
    UserRegistrationSchema,
    UserLoginSchema,
    UserUpdateSchema,
)

auth_bp = Blueprint("auth", __name__)

# 初始化Schema实例
user_registration_schema = UserRegistrationSchema()
user_login_schema = UserLoginSchema()
user_update_schema = UserUpdateSchema()


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    用户注册
    
    请求体:
        {
            "username": "用户名",
            "email": "邮箱",
            "password": "密码",
            "full_name": "全名（可选）"
        }
    """
    data = request.get_json()

    # 使用Schema验证数据
    try:
        validated_data = user_registration_schema.load(data)
    except ValidationError as err:
        return jsonify({"success": False, "error": "数据验证失败", "details": err.messages}), 400

    username = validated_data["username"]
    email = validated_data["email"]
    password = validated_data["password"]
    full_name = validated_data.get("full_name")

    # 检查用户名是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({"success": False, "error": "用户名已存在"}), 400

    # 检查邮箱是否已存在
    if User.query.filter_by(email=email).first():
        return jsonify({"success": False, "error": "邮箱已被注册"}), 400

    # 创建新用户
    user = User.create_user(
        username=username,
        email=email,
        password=password,
        full_name=full_name
    )

    try:
        db.session.add(user)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "注册成功",
            "data": user.to_dict(include_timestamps=False)
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": f"注册失败: {str(e)}"}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    用户登录
    
    请求体:
        {
            "username": "用户名或邮箱",
            "password": "密码"
        }
    """
    data = request.get_json()

    # 使用Schema验证数据
    try:
        validated_data = user_login_schema.load(data)
    except ValidationError as err:
        return jsonify({"success": False, "error": "数据验证失败", "details": err.messages}), 400

    username_or_email = validated_data["username"]
    password = validated_data["password"]

    # 查找用户（支持用户名或邮箱登录）
    user = User.query.filter(
        (User.username == username_or_email) | (User.email == username_or_email)
    ).first()

    # 验证用户和密码
    if not user or not user.check_password(password):
        return jsonify({"success": False, "error": "用户名或密码错误"}), 401

    # 检查用户是否激活
    if not user.is_active:
        return jsonify({"success": False, "error": "账号已被禁用"}), 403

    # 更新最后登录时间
    user.last_login = datetime.utcnow()
    db.session.commit()

    # 生成 JWT Token
    access_token = create_access_token(
        identity=user.id,
        additional_claims={"role": user.role, "username": user.username}
    )
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        "success": True,
        "message": "登录成功",
        "data": {
            "user": user.to_dict(include_timestamps=False),
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    })


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """
    刷新 Access Token
    
    需要在 Authorization header 中提供 Refresh Token
    """
    identity = get_jwt_identity()
    user = User.query.get(identity)

    if not user or not user.is_active:
        return jsonify({"success": False, "error": "用户不存在或已被禁用"}), 401

    access_token = create_access_token(
        identity=user.id,
        additional_claims={"role": user.role, "username": user.username}
    )

    return jsonify({
        "success": True,
        "data": {"access_token": access_token}
    })


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    """
    获取当前登录用户信息
    
    需要在 Authorization header 中提供 Access Token
    """
    identity = get_jwt_identity()
    user = User.query.get(identity)

    if not user:
        return jsonify({"success": False, "error": "用户不存在"}), 404

    return jsonify({
        "success": True,
        "data": user.to_dict()
    })


@auth_bp.route("/me", methods=["PUT"])
@jwt_required()
def update_current_user():
    """
    更新当前用户信息
    
    请求体:
        {
            "full_name": "新的全名",
            "email": "新的邮箱"
        }
    """
    identity = get_jwt_identity()
    user = User.query.get(identity)

    if not user:
        return jsonify({"success": False, "error": "用户不存在"}), 404

    data = request.get_json()

    # 使用Schema验证数据
    try:
        validated_data = user_update_schema.load(data)
    except ValidationError as err:
        return jsonify({"success": False, "error": "数据验证失败", "details": err.messages}), 400

    # 更新允许修改的字段
    if "full_name" in validated_data:
        user.full_name = validated_data["full_name"]

    if "email" in validated_data:
        new_email = validated_data["email"]
        # 检查新邮箱是否已被其他用户使用
        existing = User.query.filter(User.email == new_email, User.id != user.id).first()
        if existing:
            return jsonify({"success": False, "error": "邮箱已被其他用户使用"}), 400
        user.email = new_email

    try:
        db.session.commit()
        return jsonify({
            "success": True,
            "message": "更新成功",
            "data": user.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": f"更新失败: {str(e)}"}), 500


@auth_bp.route("/change-password", methods=["POST"])
@jwt_required()
def change_password():
    """
    修改密码
    
    请求体:
        {
            "old_password": "旧密码",
            "new_password": "新密码"
        }
    """
    identity = get_jwt_identity()
    user = User.query.get(identity)

    if not user:
        return jsonify({"success": False, "error": "用户不存在"}), 404

    data = request.get_json()

    if not data or not data.get("old_password") or not data.get("new_password"):
        return jsonify({"success": False, "error": "缺少必填字段"}), 400

    # 验证旧密码
    if not user.check_password(data["old_password"]):
        return jsonify({"success": False, "error": "旧密码错误"}), 401

    # 设置新密码
    user.set_password(data["new_password"])

    try:
        db.session.commit()
        return jsonify({"success": True, "message": "密码修改成功"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": f"密码修改失败: {str(e)}"}), 500


@auth_bp.route("/users", methods=["GET"])
@jwt_required()
def list_users():
    """
    获取用户列表（仅管理员）
    """
    # 获取当前用户角色
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"success": False, "error": "权限不足"}), 403

    users = User.query.all()
    return jsonify({
        "success": True,
        "data": [user.to_dict() for user in users]
    })

