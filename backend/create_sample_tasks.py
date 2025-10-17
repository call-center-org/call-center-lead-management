"""
为现有数据包创建示例外呼任务和通话记录
"""

from app import create_app, db
from app.models import LeadPackage, DialTask, Call, CallTag
from datetime import datetime, timedelta
import random


def create_sample_tasks():
    """为前5个数据包创建示例外呼任务和通话记录"""
    app = create_app()

    with app.app_context():
        # 获取前5个数据包
        packages = LeadPackage.query.limit(5).all()

        if not packages:
            print("❌ 没有找到数据包")
            return

        print(f"📦 找到 {len(packages)} 个数据包，开始创建测试数据...\n")

        for package in packages:
            print(f"处理数据包: {package.name} (ID: {package.id})")

            # 为每个数据包创建2个外呼任务
            for task_num in range(1, 3):
                start_date = datetime.now() - timedelta(days=random.randint(1, 30))

                task = DialTask(
                    package_id=package.id,
                    task_name=f"{package.name[:15]}... - 第{task_num}次外呼",
                    description=f"外呼任务 {task_num}：针对 {package.industry} 行业的客户进行跟进",
                    start_time=start_date,
                    end_time=start_date + timedelta(hours=8),
                    status="completed" if task_num == 1 else "in_progress",
                )
                db.session.add(task)
                db.session.flush()

                print(f"  ✅ 创建外呼任务: {task.task_name}")

                # 为每个任务创建10-20条通话记录
                num_calls = random.randint(10, 20)
                results = ["connected", "no_answer", "busy", "voicemail"]

                # 统计数据
                connected_count = 0
                interested_count = 0

                for call_num in range(num_calls):
                    # 按真实概率分配结果
                    result = random.choices(
                        results,
                        weights=[
                            30,
                            40,
                            20,
                            10,
                        ],  # 30%接通，40%未接，20%忙碌，10%语音信箱
                    )[0]

                    is_connected = result == "connected"
                    if is_connected:
                        connected_count += 1

                    # 生成电话号码
                    phone = f"138{random.randint(10000000, 99999999)}"

                    # 通话时长（接通的才有）
                    duration = random.randint(30, 300) if is_connected else 0

                    # 客户信息（接通的才有）
                    customer_names = [
                        "张三",
                        "李四",
                        "王五",
                        "赵六",
                        "孙七",
                        "周八",
                        "吴九",
                        "郑十",
                    ]
                    companies = [
                        "科技公司",
                        "贸易公司",
                        "制造企业",
                        "服务公司",
                        "咨询公司",
                        "教育机构",
                    ]

                    customer_name = (
                        random.choice(customer_names) if is_connected else None
                    )
                    company = (
                        f"{random.choice(customer_names)[0]}{random.choice(companies)}"
                        if is_connected
                        else None
                    )

                    # 备注
                    notes_list = (
                        [
                            "客户态度友好，表示有兴趣进一步了解",
                            "客户暂时没有需求，可以后续跟进",
                            "客户表示需要考虑一下",
                            "客户很感兴趣，要求发送详细资料",
                            "客户已有合作伙伴，暂不考虑",
                            "通话质量良好，沟通顺畅",
                        ]
                        if is_connected
                        else [
                            "未接通",
                            "电话无人接听",
                            "对方正忙",
                        ]
                    )

                    call_time = start_date + timedelta(minutes=call_num * 15)

                    call = Call(
                        task_id=task.id,
                        phone_number=phone,
                        call_time=call_time,
                        duration=duration,
                        result=result,
                        customer_name=customer_name,
                        company=company,
                        notes=random.choice(notes_list),
                    )
                    db.session.add(call)
                    db.session.flush()

                    # 为接通的电话添加标签
                    if is_connected:
                        # 意向等级
                        interest_levels = ["high", "medium", "low"]
                        interest_weights = [
                            20,
                            50,
                            30,
                        ]  # 20%高意向，50%中意向，30%低意向
                        interest = random.choices(
                            interest_levels, weights=interest_weights
                        )[0]

                        if interest == "high":
                            interested_count += 1

                        tag1 = CallTag(
                            call_id=call.id,
                            tag_name="意向等级",
                            tag_value=interest,
                            tag_type="interest",
                        )
                        db.session.add(tag1)

                        # 行业标签
                        industries = ["科技", "教育", "金融", "医疗", "制造", "零售"]
                        tag2 = CallTag(
                            call_id=call.id,
                            tag_name="客户行业",
                            tag_value=random.choice(industries),
                            tag_type="industry",
                        )
                        db.session.add(tag2)

                # 更新任务统计
                task.total_calls = num_calls
                task.connected_calls = connected_count
                task.interested_calls = interested_count

                print(
                    f"    📞 创建 {num_calls} 条通话记录 (接通: {connected_count}, 意向: {interested_count})"
                )

            # 重新计算数据包指标
            package.calculate_metrics()
            print(
                f"  📊 更新数据包指标 - 接通率: {package.contact_rate:.2f}%, 意向率: {package.interest_rate:.2f}%\n"
            )

        # 提交所有更改
        db.session.commit()
        print("✅ 所有测试数据创建完成！")

        # 显示摘要
        print("\n" + "=" * 60)
        print("📊 数据摘要")
        print("=" * 60)
        total_tasks = DialTask.query.count()
        total_calls = Call.query.count()
        total_tags = CallTag.query.count()

        print(f"外呼任务总数: {total_tasks}")
        print(f"通话记录总数: {total_calls}")
        print(f"通话标签总数: {total_tags}")
        print("=" * 60)


if __name__ == "__main__":
    create_sample_tasks()
