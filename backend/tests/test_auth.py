"""
Authentication API tests
"""

import pytest
from app import db
from app.models import User


class TestUserRegistration:
    """测试用户注册"""

    def test_register_success(self, client):
        """测试成功注册"""
        response = client.post(
            "/api/auth/register",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "password123",
                "full_name": "New User",
            },
        )

        assert response.status_code == 201
        data = response.get_json()
        assert data["success"] is True
        assert data["data"]["username"] == "newuser"
        assert data["data"]["email"] == "newuser@example.com"

    def test_register_duplicate_username(self, client, sample_user):
        """测试注册重复用户名"""
        response = client.post(
            "/api/auth/register",
            json={
                "username": "sampleuser",
                "email": "another@example.com",
                "password": "password123",
            },
        )

        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "用户名已存在" in data["error"]

    def test_register_invalid_email(self, client):
        """测试无效邮箱"""
        response = client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "invalid-email",
                "password": "password123",
            },
        )

        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "数据验证失败" in data["error"]

    def test_register_short_password(self, client):
        """测试密码过短"""
        response = client.post(
            "/api/auth/register",
            json={"username": "testuser", "email": "test@example.com", "password": "123"},
        )

        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False


class TestUserLogin:
    """测试用户登录"""

    def test_login_success(self, client, sample_user):
        """测试成功登录"""
        response = client.post(
            "/api/auth/login",
            json={"username": "sampleuser", "password": "sample123"},
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert "access_token" in data["data"]
        assert "refresh_token" in data["data"]
        assert data["data"]["user"]["username"] == "sampleuser"

    def test_login_with_email(self, client, sample_user):
        """测试使用邮箱登录"""
        response = client.post(
            "/api/auth/login",
            json={"username": "sample@example.com", "password": "sample123"},
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True

    def test_login_wrong_password(self, client, sample_user):
        """测试错误密码"""
        response = client.post(
            "/api/auth/login",
            json={"username": "sampleuser", "password": "wrongpassword"},
        )

        assert response.status_code == 401
        data = response.get_json()
        assert data["success"] is False

    def test_login_nonexistent_user(self, client):
        """测试不存在的用户"""
        response = client.post(
            "/api/auth/login",
            json={"username": "nonexistent", "password": "password123"},
        )

        assert response.status_code == 401
        data = response.get_json()
        assert data["success"] is False


class TestProtectedRoutes:
    """测试受保护的路由"""

    def test_get_current_user_success(self, client, auth_headers):
        """测试获取当前用户信息"""
        response = client.get("/api/auth/me", headers=auth_headers)

        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert data["data"]["username"] == "testuser"

    def test_get_current_user_without_token(self, client):
        """测试未提供token"""
        response = client.get("/api/auth/me")

        assert response.status_code == 401

    def test_update_user_info(self, client, auth_headers):
        """测试更新用户信息"""
        response = client.put(
            "/api/auth/me",
            headers=auth_headers,
            json={"full_name": "Updated Name", "email": "updated@example.com"},
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert data["data"]["full_name"] == "Updated Name"
        assert data["data"]["email"] == "updated@example.com"

