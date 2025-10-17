"""
修复已导入数据的接通率
将没有通话记录的数据包的接通率设置为0
"""

import sys
from app import create_app, db
from app.models import LeadPackage


def fix_contact_rates():
    """修复接通率数据"""

    app = create_app()

    with app.app_context():
        print("🔧 开始修复接通率数据...\n")

        # 获取所有数据包
        packages = LeadPackage.query.all()
        fixed_count = 0

        for package in packages:
            # 检查是否有通话记录
            stats = package.get_call_statistics()

            if not stats["has_call_data"]:
                # 没有通话记录，设置接通率为0
                old_rate = package.contact_rate
                package.contact_rate = 0.0
                package.interest_rate = 0.0

                print(
                    f"✅ 修复: {package.name} - 接通率从 {old_rate:.2%} 改为 0.00%"
                )
                fixed_count += 1
            else:
                # 有通话记录，从通话数据计算
                old_rate = package.contact_rate
                package.calculate_metrics()

                print(
                    f"📊 更新: {package.name} - 接通率从 {old_rate:.2%} 改为 {package.contact_rate:.2%}"
                )
                fixed_count += 1

        # 提交更改
        try:
            db.session.commit()
            print(f"\n✅ 成功修复 {fixed_count} 个数据包的接通率")
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ 提交失败: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    fix_contact_rates()

