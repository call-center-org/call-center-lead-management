"""
Model tests
"""

import pytest
from app import db
from app.models import User, LeadPackage, DialTask, Call
from datetime import datetime


class TestUserModel:
    """测试User模型"""

    def test_create_user(self):
        """测试创建用户"""
        user = User.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            full_name="Test User",
        )

        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
        assert user.password_hash is not None
        assert user.password_hash != "password123"  # 密码应该被哈希

    def test_password_hashing(self):
        """测试密码哈希"""
        user = User.create_user(
            username="testuser", email="test@example.com", password="password123"
        )

        assert user.check_password("password123") is True
        assert user.check_password("wrongpassword") is False

    def test_user_to_dict(self, sample_user):
        """测试用户序列化"""
        user_dict = sample_user.to_dict()

        assert user_dict["username"] == "sampleuser"
        assert user_dict["email"] == "sample@example.com"
        assert "password_hash" not in user_dict  # 密码不应该被序列化
        assert "created_at" in user_dict


class TestLeadPackageModel:
    """测试LeadPackage模型"""

    def test_create_package(self):
        """测试创建数据包"""
        package = LeadPackage(
            name="测试数据包",
            source="采买",
            industry="高中",
            region="江苏",
            total_leads=1000,
            valid_leads=900,
            cost_per_lead=2.5,
        )
        package.calculate_metrics()  # 计算指标
        db.session.add(package)
        db.session.commit()

        assert package.id is not None
        assert package.name == "测试数据包"
        assert package.total_cost == 2500.0  # total_leads * cost_per_lead = 1000 * 2.5

    def test_package_to_dict(self, sample_package):
        """测试数据包序列化"""
        package_dict = sample_package.to_dict()

        assert package_dict["name"] == "测试数据包"
        assert package_dict["source"] == "采买"
        assert package_dict["total_leads"] == 1000
        assert package_dict["valid_leads"] == 900

    def test_calculate_metrics(self, sample_package, sample_task):
        """测试计算指标"""
        # 添加一些通话记录
        call1 = Call(
            task_id=sample_task.id,
            phone_number="13800138000",
            call_time=datetime(2025, 10, 17, 10, 0, 0),
            duration=60,
            result="connected",
        )
        call2 = Call(
            task_id=sample_task.id,
            phone_number="13800138001",
            call_time=datetime(2025, 10, 17, 10, 5, 0),
            duration=0,
            result="no_answer",
        )
        db.session.add_all([call1, call2])
        db.session.commit()

        # 更新任务统计
        sample_task.total_calls = 2
        sample_task.connected_calls = 1
        sample_task.interested_calls = 1
        db.session.commit()

        # 计算指标
        sample_package.calculate_metrics()

        # 验证接通率：1个接通 / 2个通话 = 0.5
        assert sample_package.contact_rate == 0.5  # 1/2
        # 验证总成本已计算
        assert sample_package.total_cost == 1000.0  # total_leads * cost_per_lead = 1000 * 1.0


class TestDialTaskModel:
    """测试DialTask模型"""

    def test_create_task(self, sample_package):
        """测试创建外呼任务"""
        task = DialTask(
            package_id=sample_package.id,
            task_name="测试任务",
            description="任务描述",
            start_time=datetime(2025, 10, 17, 9, 0, 0),
            status="pending",
        )
        db.session.add(task)
        db.session.commit()

        assert task.id is not None
        assert task.package_id == sample_package.id
        assert task.task_name == "测试任务"
        assert task.status == "pending"

    def test_task_to_dict(self, sample_task):
        """测试任务序列化"""
        task_dict = sample_task.to_dict()

        assert task_dict["task_name"] == "测试任务"
        assert task_dict["status"] == "pending"
        assert "package_id" in task_dict

    def test_task_package_relationship(self, sample_package, sample_task):
        """测试任务和数据包的关系"""
        assert sample_task.package.id == sample_package.id
        assert sample_task in sample_package.dial_tasks.all()

