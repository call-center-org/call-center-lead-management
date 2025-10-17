"""
生成数据包标签汇总数据
"""

from app import create_app, db
from app.models import LeadPackage, PackageTagSummary, CallTag, DialTask
from sqlalchemy import func


def generate_tag_summaries():
    """为每个数据包生成标签汇总"""
    app = create_app()

    with app.app_context():
        # 清空现有标签汇总
        print("🗑️  清除现有标签汇总...")
        PackageTagSummary.query.delete()
        db.session.commit()
        print("✅ 清除完成\n")

        # 获取所有数据包
        packages = LeadPackage.query.all()

        if not packages:
            print("❌ 没有找到数据包")
            return

        print(f"📦 找到 {len(packages)} 个数据包，开始生成标签汇总...\n")

        for package in packages:
            print(f"处理数据包: {package.name} (ID: {package.id})")

            # 获取该数据包的所有外呼任务ID
            task_ids = [task.id for task in package.dial_tasks.all()]

            if not task_ids:
                print(f"  ⏭️  跳过：没有外呼任务\n")
                continue

            # 统计该数据包所有通话的标签
            # 按 tag_name 和 tag_value 分组统计
            from app.models import Call

            tag_stats = (
                db.session.query(
                    CallTag.tag_name,
                    CallTag.tag_value,
                    func.count(CallTag.id).label("tag_count"),
                )
                .join(Call, CallTag.call_id == Call.id)
                .filter(Call.task_id.in_(task_ids))
                .group_by(CallTag.tag_name, CallTag.tag_value)
                .all()
            )

            # 计算总标签数（按 tag_name 分组）
            tag_totals = {}
            for stat in tag_stats:
                tag_name = stat.tag_name
                if tag_name not in tag_totals:
                    tag_totals[tag_name] = 0
                tag_totals[tag_name] += stat.tag_count

            # 创建标签汇总记录
            summaries_created = 0
            for stat in tag_stats:
                tag_name = stat.tag_name
                tag_value = stat.tag_value
                tag_count = stat.tag_count

                # 计算占比
                percentage = (
                    tag_count / tag_totals[tag_name] if tag_totals[tag_name] > 0 else 0
                )

                summary = PackageTagSummary(
                    package_id=package.id,
                    tag_name=tag_name,
                    tag_value=tag_value,
                    tag_count=tag_count,
                    percentage=percentage,
                )
                db.session.add(summary)
                summaries_created += 1

            db.session.commit()
            print(f"  ✅ 创建 {summaries_created} 条标签汇总记录\n")

        print("✅ 所有标签汇总生成完成！")

        # 显示摘要
        print("\n" + "=" * 60)
        print("📊 数据摘要")
        print("=" * 60)
        total_packages = LeadPackage.query.count()
        total_summaries = PackageTagSummary.query.count()

        print(f"数据包总数: {total_packages}")
        print(f"标签汇总总数: {total_summaries}")
        print(
            f"平均每个数据包: {total_summaries / total_packages:.1f} 条汇总"
            if total_packages > 0
            else "0"
        )
        print("=" * 60)


if __name__ == "__main__":
    generate_tag_summaries()

