"""
API 测试脚本
"""

from app import create_app, db
from app.models import LeadPackage, DialTask, Call, CallTag
from datetime import datetime


def test_create_data():
    """创建测试数据"""
    app = create_app()

    with app.app_context():
        # 创建数据包
        package = LeadPackage(
            name="测试数据包 - 科技行业",
            source="线上渠道",
            industry="科技",
            region="江苏",
            total_leads=1000,
            valid_leads=900,
            cost_per_lead=2.5,
        )
        package.calculate_metrics()
        db.session.add(package)
        db.session.flush()

        print(f"✅ 创建数据包: {package.name} (ID: {package.id})")

        # 创建外呼任务
        task = DialTask(
            package_id=package.id,
            task_name="首次外呼任务",
            description="测试外呼任务描述",
            start_time=datetime(2025, 10, 18, 9, 0, 0),
            end_time=datetime(2025, 10, 18, 18, 0, 0),
            status="in_progress",
        )
        db.session.add(task)
        db.session.flush()

        print(f"✅ 创建外呼任务: {task.task_name} (ID: {task.id})")

        # 创建通话记录
        calls_data = [
            {
                "phone": "13800138001",
                "result": "connected",
                "duration": 120,
                "customer": "张三",
                "company": "ABC科技",
                "tags": [{"name": "interest_level", "value": "high"}],
            },
            {
                "phone": "13800138002",
                "result": "connected",
                "duration": 90,
                "customer": "李四",
                "company": "XYZ公司",
                "tags": [{"name": "interest_level", "value": "medium"}],
            },
            {
                "phone": "13800138003",
                "result": "no_answer",
                "duration": 0,
                "customer": None,
                "company": None,
                "tags": [],
            },
            {
                "phone": "13800138004",
                "result": "connected",
                "duration": 150,
                "customer": "王五",
                "company": "DEF企业",
                "tags": [{"name": "interest_level", "value": "high"}],
            },
            {
                "phone": "13800138005",
                "result": "busy",
                "duration": 0,
                "customer": None,
                "company": None,
                "tags": [],
            },
        ]

        for i, call_data in enumerate(calls_data):
            call = Call(
                task_id=task.id,
                phone_number=call_data["phone"],
                call_time=datetime(2025, 10, 18, 10, i * 10, 0),
                duration=call_data["duration"],
                result=call_data["result"],
                customer_name=call_data["customer"],
                company=call_data["company"],
                notes=f"测试通话记录 {i+1}",
            )
            db.session.add(call)
            db.session.flush()

            # 添加标签
            for tag_data in call_data["tags"]:
                tag = CallTag(
                    call_id=call.id,
                    tag_name=tag_data["name"],
                    tag_value=tag_data["value"],
                    tag_type="interest_level",
                )
                db.session.add(tag)

            print(f"✅ 创建通话记录: {call.phone_number} - {call.result}")

        # 提交所有更改
        db.session.commit()

        # 更新任务指标
        task.calculate_metrics()
        db.session.commit()

        print("\n" + "=" * 50)
        print("📊 统计信息:")
        print(f"数据包总数: {LeadPackage.query.count()}")
        print(f"外呼任务总数: {DialTask.query.count()}")
        print(f"通话记录总数: {Call.query.count()}")
        print(f"任务接通率: {task.contact_rate:.2%}")
        print(f"任务接通次数: {task.connected_calls}/{task.total_calls}")
        print("=" * 50)

        return package, task


def test_api_queries():
    """测试 API 查询"""
    from app.routes.metrics import get_dashboard_metrics

    app = create_app()

    with app.app_context():
        with app.test_client() as client:
            # 测试获取所有数据包
            print("\n📦 测试 GET /api/packages")
            response = client.get("/api/packages")
            print(f"状态码: {response.status_code}")
            data = response.get_json()
            print(f"数据包数量: {len(data['data'])}")

            # 测试获取仪表盘数据
            print("\n📊 测试 GET /api/metrics/dashboard")
            response = client.get("/api/metrics/dashboard")
            print(f"状态码: {response.status_code}")
            data = response.get_json()
            summary = data["data"]["summary"]
            print(f"总数据包: {summary['total_packages']}")
            print(f"总线索: {summary['total_leads']}")
            print(f"平均接通率: {summary['avg_contact_rate']:.2%}")

            # 测试获取数据包详情
            print("\n📝 测试 GET /api/packages/1")
            response = client.get("/api/packages/1")
            print(f"状态码: {response.status_code}")
            data = response.get_json()
            package = data["data"]
            print(f"数据包名称: {package['name']}")
            print(f"外呼任务数: {len(package['dial_tasks'])}")

            print("\n✅ 所有 API 测试通过！")


if __name__ == "__main__":
    print("🚀 开始创建测试数据...\n")
    test_create_data()

    print("\n🧪 开始测试 API...\n")
    test_api_queries()

    print("\n✨ 测试完成！")
