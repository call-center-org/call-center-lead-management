"""
Pytest configuration and fixtures
"""

import pytest
from app import create_app, db
from app.models import User, LeadPackage, DialTask


@pytest.fixture(scope="function", autouse=True)
def app():
    """创建测试应用"""
    app = create_app("testing")
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def _app_ctx(app):
    """自动应用app context"""
    with app.app_context():
        yield


@pytest.fixture
def client(app):
    """创建测试客户端"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """创建CLI测试runner"""
    return app.test_cli_runner()


@pytest.fixture
def auth_headers(client):
    """创建认证headers（包含有效的JWT token）"""
    # 创建测试用户
    user = User.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )
    db.session.add(user)
    db.session.commit()
    
    # 登录获取token
    response = client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "testpass123"
    })
    
    data = response.get_json()
    token = data["data"]["access_token"]
    
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_user():
    """创建示例用户"""
    user = User.create_user(
        username="sampleuser",
        email="sample@example.com",
        password="sample123",
        full_name="Sample User"
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def sample_package():
    """创建示例数据包"""
    package = LeadPackage(
        name="测试数据包",
        source="采买",
        industry="高中",
        region="江苏",
        total_leads=1000,
        valid_leads=900,
        cost_per_lead=1.0
    )
    db.session.add(package)
    db.session.commit()
    return package


@pytest.fixture
def sample_task(sample_package):
    """创建示例外呼任务"""
    from datetime import datetime
    
    task = DialTask(
        package_id=sample_package.id,
        task_name="测试任务",
        description="测试任务描述",
        start_time=datetime(2025, 10, 17, 9, 0, 0),
        status="pending"
    )
    db.session.add(task)
    db.session.commit()
    return task

