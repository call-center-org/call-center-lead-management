"""
Excel 数据批量导入脚本
根据实际Excel数据导入到系统
"""

import sys
from app import create_app, db
from app.models import LeadPackage
from datetime import datetime


def import_data():
    """导入Excel中的历史数据"""

    # Excel数据（从图片提取）
    excel_data = [
        {
            "name": "dyac1-20250826-高中加购.cs",
            "company": "107847",
            "total": 1000,
            "valid": 1000,
            "region": "禹州",
            "date": "0826",
            "grade": "高中",
            "source": "采买",
        },
        {
            "name": "dy3-20250905-高中加购.csv",
            "company": "107847",
            "total": 5000,
            "valid": 5000,
            "region": "禹州",
            "date": "0905",
            "grade": "高中",
            "source": "采买",
        },
        {
            "name": "dy2-20250908-高中加购.cSW",
            "company": "107847",
            "total": 5000,
            "valid": 5000,
            "region": "禹州",
            "date": "0908",
            "grade": "高中",
            "source": "采买",
        },
        {
            "name": "dy3-20250908-高中加购.csv",
            "company": "107847",
            "total": 5000,
            "valid": 5000,
            "region": "禹州",
            "date": "0908",
            "grade": "高中",
            "source": "采买",
        },
        {
            "name": "dy1-20250905-高中加购.cs",
            "company": "107849",
            "total": 5000,
            "valid": 5000,
            "region": "宜宾",
            "date": "0905",
            "grade": "高中",
            "source": "采买",
        },
        {
            "name": "dyac2-20250826-高中加购.csv",
            "company": "107848",
            "total": 1000,
            "valid": 1000,
            "region": "淮安",
            "date": "0826",
            "grade": "高中",
            "source": "采买",
        },
        {
            "name": "dy2-20250905-高中加购.cs",
            "company": "107848",
            "total": 5000,
            "valid": 5000,
            "region": "淮安",
            "date": "0905",
            "grade": "高中",
            "source": "采买",
        },
        {
            "name": "dy1-20250908-高中加购.csv",
            "company": "107848",
            "total": 5000,
            "valid": 5000,
            "region": "淮安",
            "date": "0908",
            "grade": "高中",
            "source": "采买",
        },
        {
            "name": "dy1-20250910-高中加购.csv",
            "company": "107848",
            "total": 5000,
            "valid": 5000,
            "region": "淮安",
            "date": "0910",
            "grade": "高中",
            "source": "采买",
        },
        {
            "name": "dy_20250913-高中加购-补.csv",
            "company": "107848",
            "total": 1253,
            "valid": 1253,
            "region": "淮安",
            "date": "0913",
            "grade": "高中",
            "source": "采买",
        },
        {
            "name": "dy-20250913-高中加购.cSV",
            "company": "107848",
            "total": 3747,
            "valid": 3747,
            "region": "淮安",
            "date": "0913",
            "grade": "高中",
            "source": "采买",
        },
        {
            "name": "dyac2-20250920 - 高中加购.csv",
            "company": "107847",
            "total": 5000,
            "valid": 5000,
            "region": "禹州",
            "date": "0920",
            "grade": "高中",
            "source": "采买",
        },
        {
            "name": "dyac1-20250920 - 高中加购.csv",
            "company": "107848",
            "total": 5000,
            "valid": 5000,
            "region": "淮安",
            "date": "0920",
            "grade": "高中",
            "source": "采买",
        },
        {
            "name": "dyac2-20250922-高中加购.csy",
            "company": "107848",
            "total": 5000,
            "valid": 5000,
            "region": "淮安",
            "date": "0922",
            "grade": "高中",
            "source": "采买",
        },
        {
            "name": "dyac1-20250922-高中加购.csv",
            "company": "107848",
            "total": 5000,
            "valid": 5000,
            "region": "淮安",
            "date": "0922",
            "grade": "高中",
            "source": "采买",
        },
        {
            "name": "dyac-20250923-高中加购.csv",
            "company": "107848",
            "total": 15000,
            "valid": 15000,
            "region": "淮安",
            "date": "0923",
            "grade": "高中",
            "source": "采买",
        },
        {
            "name": "dy-20251014-高中加购.csv",
            "company": "107848",
            "total": 10000,
            "valid": 10000,
            "region": "淮安",
            "date": "1014",
            "grade": "高中",
            "source": "采买",
        },
        {
            "name": "dy-20250717-Gj单.csv",
            "company": "107848",
            "total": 15000,
            "valid": 15000,
            "region": "淮安",
            "date": "0717",
            "grade": "高中",
            "source": "练习",
        },
        {
            "name": "dy-20250718-Gj单.csv",
            "company": "107848",
            "total": 15000,
            "valid": 15000,
            "region": "淮安",
            "date": "0718",
            "grade": "高中",
            "source": "练习",
        },
        {
            "name": "tmc-20251016-高中加购.csv",
            "company": "107848",
            "total": 10000,
            "valid": 10000,
            "region": "淮安",
            "date": "1016",
            "grade": "高中",
            "source": "采买",
        },
    ]

    app = create_app()

    with app.app_context():
        print(f"🚀 开始导入 {len(excel_data)} 条历史数据...\n")

        success_count = 0
        skip_count = 0
        error_count = 0

        for index, data in enumerate(excel_data, 1):
            try:
                # 检查是否已存在
                existing = LeadPackage.query.filter_by(name=data["name"]).first()
                if existing:
                    print(f"⚠️  [{index}/{len(excel_data)}] 跳过重复: {data['name']}")
                    skip_count += 1
                    continue

                # 创建数据包
                package = LeadPackage(
                    name=data["name"],
                    source=data["source"],
                    industry=data["grade"],
                    region=data["region"],
                    total_leads=data["total"],
                    valid_leads=data["valid"],
                    cost_per_lead=1.0,  # 默认单条成本1元
                )

                # 计算指标
                package.calculate_metrics()

                # 保存
                db.session.add(package)
                db.session.flush()

                print(
                    f"✅ [{index}/{len(excel_data)}] 导入成功: {data['name']} (ID: {package.id})"
                )
                success_count += 1

                # 每10条提交一次
                if index % 10 == 0:
                    db.session.commit()
                    print(f"💾 已提交 {index} 条记录\n")

            except Exception as e:
                print(f"❌ [{index}/{len(excel_data)}] 导入失败: {data['name']}")
                print(f"   错误: {str(e)}\n")
                error_count += 1
                db.session.rollback()
                continue

        # 最终提交
        try:
            db.session.commit()
            print("\n" + "=" * 60)
            print("📊 导入完成统计:")
            print(f"   ✅ 成功: {success_count} 条")
            print(f"   ⚠️  跳过: {skip_count} 条")
            print(f"   ❌ 失败: {error_count} 条")
            print(f"   📦 总计: {len(excel_data)} 条")
            print("=" * 60)

            # 显示数据库统计
            total_packages = LeadPackage.query.count()
            total_leads = (
                db.session.query(db.func.sum(LeadPackage.total_leads)).scalar() or 0
            )
            print(f"\n📈 当前数据库统计:")
            print(f"   数据包总数: {total_packages}")
            print(f"   线索总量: {total_leads:,}")

        except Exception as e:
            db.session.rollback()
            print(f"\n❌ 提交失败: {str(e)}")


if __name__ == "__main__":
    import_data()
