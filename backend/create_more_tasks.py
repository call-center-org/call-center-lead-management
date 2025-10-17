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

                    # 为接通的电话添加标签（使用真实的16个标签）
                    if is_connected:
                        # 真实标签定义（基于PRD文档）
                        # 成功类（2个）：AS1, AS2
                        # 可跟进类（8个）：AF2, AF3, AF4, AF5, AF11, AF12, AF13, AF14
                        # 无效类（5个）：AN1, AN2, AN3, AN4, AOT
                        # 未处理类（1个）：AG
                        
                        # 按真实业务概率分配标签
                        tag_distribution = [
                            ("AS1", "成功单9元", 5),          # 5% 成功单9元
                            ("AS2", "成功单1元", 8),          # 8% 成功单1元
                            ("AF11", "高中家长", 12),         # 12% 高中家长
                            ("AF12", "初中家长", 10),         # 10% 初中家长
                            ("AF13", "小学家长", 8),          # 8% 小学家长
                            ("AF14", "学生本人", 5),          # 5% 学生本人
                            ("AF3", "加微信成功挂断", 10),    # 10% 加微信
                            ("AF4", "付费环节挂断", 6),       # 6% 付费环节
                            ("AF2", "在忙/晚点再说", 15),     # 15% 在忙
                            ("AF5", "没说话，直接挂断", 8),   # 8% 没说话
                            ("AN2", "明确不需要/非目标人", 8), # 8% 明拒
                            ("AN4", "已报名/已购买", 3),      # 3% 已购买
                            ("AN3", "语音助手", 1),           # 1% 语音助手
                            ("AOT", "其他", 1),               # 1% 其他
                        ]
                        
                        # 选择标签
                        tag_codes = [t[0] for t in tag_distribution]
                        tag_names = [t[1] for t in tag_distribution]
                        tag_weights = [t[2] for t in tag_distribution]
                        
                        selected_index = random.choices(
                            range(len(tag_codes)),
                            weights=tag_weights
                        )[0]
                        
                        tag_code = tag_codes[selected_index]
                        tag_name = tag_names[selected_index]
                        
                        # 成功单计数
                        if tag_code in ["AS1", "AS2"]:
                            interested_count += 1
                        
                        # 保存标签
                        tag = CallTag(
                            call_id=call.id,
                            tag_name=tag_code,  # 使用标签代码作为tag_name
                            tag_value=tag_name,  # 使用标签含义作为tag_value
                            tag_type="result",
                        )
                        db.session.add(tag)

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
