"""
管理员路由
用于系统管理和测试数据管理
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import LeadPackage, User
from datetime import datetime, timedelta
import random

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/seed-test-data", methods=["POST"])
@jwt_required()
def seed_test_data():
    """
    生成测试数据
    需要管理员权限
    """
    # 获取当前用户
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"success": False, "message": "用户不存在"}), 404

    # 测试数据配置
    test_packages = [
        {
            "name": "ks-20251015-K12素质教育",
            "source": "快手",
            "industry": "教育培训",
            "region": "浙江",
            "total_leads": 8500,
            "valid_leads": 8200,
            "cost_per_lead": 1.2,
            "contact_rate": 0.72,
            "interest_rate": 0.18,
        },
        {
            "name": "bd-20251016-IT培训意向",
            "source": "百度",
            "industry": "职业培训",
            "region": "北京",
            "total_leads": 5000,
            "valid_leads": 4800,
            "cost_per_lead": 2.5,
            "contact_rate": 0.58,
            "interest_rate": 0.22,
        },
        {
            "name": "tt-20251017-金融理财",
            "source": "头条",
            "industry": "金融服务",
            "region": "上海",
            "total_leads": 12000,
            "valid_leads": 11500,
            "cost_per_lead": 1.8,
            "contact_rate": 0.45,
            "interest_rate": 0.12,
        },
        {
            "name": "wx-20251018-房产咨询",
            "source": "微信",
            "industry": "房地产",
            "region": "广东",
            "total_leads": 6000,
            "valid_leads": 5800,
            "cost_per_lead": 3.5,
            "contact_rate": 0.68,
            "interest_rate": 0.25,
        },
        {
            "name": "xhs-20251019-美妆护肤",
            "source": "小红书",
            "industry": "电商零售",
            "region": "四川",
            "total_leads": 15000,
            "valid_leads": 14200,
            "cost_per_lead": 0.5,
            "contact_rate": 0.78,
            "interest_rate": 0.30,
        },
        {
            "name": "dy-20251020-汽车销售",
            "source": "抖音",
            "industry": "汽车行业",
            "region": "湖北",
            "total_leads": 4500,
            "valid_leads": 4300,
            "cost_per_lead": 5.0,
            "contact_rate": 0.52,
            "interest_rate": 0.20,
        },
        {
            "name": "bd-20251021-医疗咨询",
            "source": "百度",
            "industry": "医疗健康",
            "region": "河南",
            "total_leads": 7000,
            "valid_leads": 6500,
            "cost_per_lead": 4.2,
            "contact_rate": 0.60,
            "interest_rate": 0.28,
        },
        {
            "name": "ks-20251022-家装服务",
            "source": "快手",
            "industry": "家居建材",
            "region": "山东",
            "total_leads": 9000,
            "valid_leads": 8600,
            "cost_per_lead": 1.5,
            "contact_rate": 0.70,
            "interest_rate": 0.16,
        },
        {
            "name": "tt-20251023-旅游度假",
            "source": "头条",
            "industry": "旅游服务",
            "region": "云南",
            "total_leads": 11000,
            "valid_leads": 10500,
            "cost_per_lead": 0.9,
            "contact_rate": 0.75,
            "interest_rate": 0.35,
        },
    ]

    packages_created = []
    packages_skipped = []

    for data in test_packages:
        # 检查是否已存在
        existing = LeadPackage.query.filter_by(name=data["name"]).first()
        if existing:
            packages_skipped.append(data["name"])
            continue

        # 创建数据包
        package = LeadPackage(**data)
        package.calculate_metrics()

        # 随机设置创建时间（过去7天内）
        days_ago = random.randint(0, 7)
        package.created_at = datetime.utcnow() - timedelta(days=days_ago)
        package.updated_at = package.created_at

        db.session.add(package)
        packages_created.append(data["name"])

    try:
        db.session.commit()

        # 统计信息
        all_packages = LeadPackage.query.all()
        total_leads = sum(p.total_leads for p in all_packages)
        total_cost = sum(p.total_cost for p in all_packages)
        avg_contact_rate = (
            sum(p.contact_rate for p in all_packages) / len(all_packages)
            if all_packages
            else 0
        )

        return (
            jsonify(
                {
                    "success": True,
                    "message": "测试数据生成成功",
                    "data": {
                        "created": len(packages_created),
                        "skipped": len(packages_skipped),
                        "created_packages": packages_created,
                        "skipped_packages": packages_skipped,
                        "statistics": {
                            "total_packages": len(all_packages),
                            "total_leads": total_leads,
                            "total_cost": round(total_cost, 2),
                            "avg_contact_rate": round(avg_contact_rate * 100, 1),
                        },
                    },
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"success": False, "message": f"生成测试数据失败: {str(e)}"}),
            500,
        )


@admin_bp.route("/stats", methods=["GET"])
@jwt_required()
def get_stats():
    """获取系统统计信息"""

    packages = LeadPackage.query.all()
    users = User.query.all()

    return (
        jsonify(
            {
                "success": True,
                "data": {
                    "total_packages": len(packages),
                    "total_users": len(users),
                    "total_leads": sum(p.total_leads for p in packages),
                    "total_cost": sum(p.total_cost for p in packages),
                },
            }
        ),
        200,
    )


@admin_bp.route("/clear-all-packages", methods=["POST"])
@jwt_required()
def clear_all_packages():
    """
    清除所有数据包（谨慎使用）
    需要在请求体中确认
    """
    data = request.get_json()

    if not data or data.get("confirm") != "yes":
        return (
            jsonify(
                {
                    "success": False,
                    "message": "需要确认操作，请在请求体中设置 confirm: 'yes'",
                }
            ),
            400,
        )

    try:
        count = LeadPackage.query.delete()
        db.session.commit()

        return jsonify({"success": True, "message": f"已清除 {count} 个数据包"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"清除失败: {str(e)}"}), 500
