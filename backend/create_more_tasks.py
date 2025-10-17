"""
为每个数据包创建5-10个外呼任务
"""

from app import create_app, db
from app.models import LeadPackage, DialTask, Call, CallTag
from datetime import datetime, timedelta
import random


def create_more_tasks():
    """为每个数据包创建5-10个外呼任务"""
    app = create_app()

    with app.app_context():
        # 获取所有数据包
        packages = LeadPackage.query.all()

        if not packages:
            print("❌ 没有找到数据包")
            return

        print(f"📦 找到 {len(packages)} 个数据包，开始创建更多外呼任务...\n")

        # 先删除现有的所有外呼任务和通话记录
        print("🗑️  清除现有测试数据...")
        CallTag.query.delete()
        Call.query.delete()
        DialTask.query.delete()
        db.session.commit()
        print("✅ 清除完成\n")

        for package in packages:
            print(f"处理数据包: {package.name} (ID: {package.id})")

            # 为每个数据包创建5-10个外呼任务
            num_tasks = random.randint(5, 10)

            # 计算累计外呼数，用于计算剩余数
            cumulative_calls = 0

            for task_num in range(1, num_tasks + 1):
                # 任务日期从30天前开始，逐渐递增
                days_ago = 30 - (task_num - 1) * 3
                start_date = datetime.now() - timedelta(days=days_ago)

                # 任务名称：按日期命名
                task_date_str = start_date.strftime("%m%d")

                task = DialTask(
                    package_id=package.id,
                    task_name=f"{package.name[:15]}-{task_date_str}",
                    description=f"第{task_num}次外呼任务",
                    start_time=start_date,
                    end_time=start_date + timedelta(hours=8),
                    status="completed" if task_num < num_tasks else "in_progress",
                )
                db.session.add(task)
                db.session.flush()

                # 每个任务的外呼数量（逐渐减少，模拟真实情况）
                if task_num == 1:
                    # 第一次外呼数量较多
                    num_calls = random.randint(50, 100)
                elif task_num <= 3:
                    num_calls = random.randint(30, 60)
                else:
                    # 后续外呼数量递减
                    num_calls = random.randint(15, 40)

                cumulative_calls += num_calls

                results = ["connected", "no_answer", "busy", "voicemail"]

                # 统计数据
                connected_count = 0
                interested_count = 0

                for call_num in range(num_calls):
                    # 按真实概率分配结果
                    result = random.choices(
                        results,
                        weights=[30, 40, 20, 10],
                    )[0]

                    is_connected = result == "connected"
                    if is_connected:
                        connected_count += 1

                    # 生成电话号码
                    phone = f"138{random.randint(10000000, 99999999)}"

                    # 通话时长（接通的才有）
                    duration = random.randint(30, 300) if is_connected else 0

                    # 客户信息
                    customer_names = [
                        "张三",
                        "李四",
                        "王五",
                        "赵六",
                        "孙七",
                        "周八",
                        "吴九",
                        "郑十",
                        "陈先生",
                        "刘女士",
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

                    notes_list = (
                        [
                            "客户态度友好，表示有兴趣进一步了解",
                            "客户暂时没有需求，可以后续跟进",
                            "客户表示需要考虑一下",
                            "客户很感兴趣，要求发送详细资料",
                            "客户已有合作伙伴，暂不考虑",
                            "通话质量良好，沟通顺畅",
                            "需要发送产品资料和报价",
                            "约定下周再次联系",
                        ]
                        if is_connected
                        else [
                            "未接通",
                            "电话无人接听",
                            "对方正忙",
                            "语音信箱",
                        ]
                    )

                    call_time = start_date + timedelta(minutes=call_num * 5)

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
                        interest_weights = [20, 50, 30]
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
                    f"  ✅ 任务{task_num}: {num_calls}条通话 (接通:{connected_count}, 意向:{interested_count})"
                )

            # 重新计算数据包指标
            package.calculate_metrics()
            print(f"  📊 创建{num_tasks}个任务 - 接通率: {package.contact_rate:.2f}%\n")

        # 提交所有更改
        db.session.commit()
        print("✅ 所有外呼任务创建完成！")

        # 显示摘要
        print("\n" + "=" * 60)
        print("📊 数据摘要")
        print("=" * 60)
        total_packages = LeadPackage.query.count()
        total_tasks = DialTask.query.count()
        total_calls = Call.query.count()
        total_tags = CallTag.query.count()

        print(f"数据包总数: {total_packages}")
        print(f"外呼任务总数: {total_tasks}")
        print(f"通话记录总数: {total_calls}")
        print(f"通话标签总数: {total_tags}")
        print(f"平均每个数据包: {total_tasks / total_packages:.1f} 个任务")
        print("=" * 60)


if __name__ == "__main__":
    create_more_tasks()
