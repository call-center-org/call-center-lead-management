"""
Lead Package API tests
"""

import pytest
from app import db
from app.models import LeadPackage


class TestPackageList:
    """测试数据包列表API"""

    def test_get_packages_empty(self, client):
        """测试获取空数据包列表"""
        response = client.get("/api/packages")

        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert len(data["data"]) == 0

    def test_get_packages_with_data(self, client, sample_package):
        """测试获取数据包列表"""
        response = client.get("/api/packages")

        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert len(data["data"]) == 1
        assert data["data"][0]["name"] == "测试数据包"


class TestPackageCreate:
    """测试创建数据包API"""

    def test_create_package_success(self, client):
        """测试成功创建数据包"""
        response = client.post(
            "/api/packages",
            json={
                "name": "新数据包",
                "source": "采买",
                "industry": "高中",
                "region": "江苏",
                "total_leads": 500,
                "valid_leads": 450,
                "cost_per_lead": 1.5,
            },
        )

        assert response.status_code == 201
        data = response.get_json()
        assert data["success"] is True
        assert data["data"]["name"] == "新数据包"
        assert (
            data["data"]["total_cost"] == 750.0
        )  # total_leads * cost_per_lead = 500 * 1.5

    def test_create_package_missing_fields(self, client):
        """测试缺少必填字段"""
        response = client.post(
            "/api/packages",
            json={"name": "测试"},
        )

        assert response.status_code == 400


class TestPackageDetail:
    """测试数据包详情API"""

    def test_get_package_success(self, client, sample_package):
        """测试获取数据包详情"""
        response = client.get(f"/api/packages/{sample_package.id}")

        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert data["data"]["name"] == "测试数据包"
        assert "dial_tasks" in data["data"]
        assert "tag_summaries" in data["data"]

    def test_get_package_not_found(self, client):
        """测试获取不存在的数据包"""
        response = client.get("/api/packages/99999")

        assert response.status_code == 404


class TestPackageUpdate:
    """测试更新数据包API"""

    def test_update_package_success(self, client, sample_package):
        """测试成功更新数据包"""
        response = client.put(
            f"/api/packages/{sample_package.id}",
            json={"name": "更新后的名称", "region": "上海"},
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert data["data"]["name"] == "更新后的名称"
        assert data["data"]["region"] == "上海"

    def test_update_package_not_found(self, client):
        """测试更新不存在的数据包"""
        response = client.put(
            "/api/packages/99999",
            json={"name": "测试"},
        )

        assert response.status_code == 404


class TestPackageDelete:
    """测试删除数据包API"""

    def test_delete_package_success(self, client, sample_package):
        """测试成功删除数据包"""
        package_id = sample_package.id

        response = client.delete(f"/api/packages/{package_id}")

        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True

        # 验证数据包已被删除
        package = LeadPackage.query.get(package_id)
        assert package is None

    def test_delete_package_not_found(self, client):
        """测试删除不存在的数据包"""
        response = client.delete("/api/packages/99999")

        assert response.status_code == 404
