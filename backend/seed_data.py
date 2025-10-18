"""
测试数据生成脚本
用于在生产环境生成演示数据
"""

from datetime import datetime, timedelta
import random
from app import create_app, db
from app.models import LeadPackage, User


def generate_test_packages():
    """生成测试数据包"""
    
    # 测试数据配置
    test_packages = [
        {
            "name": "dy-20251014-高中加购",
            "source": "抖音",
            "industry": "教育培训",
            "region": "江苏",
            "total_leads": 10000,
            "valid_leads": 10000,
            "cost_per_lead": 0.8,
            "contact_rate": 0.65,
            "interest_rate": 0.15,
        },
        {
            "name": "ks-20251015-K12素质教育",
            "source": "快手",
            "industry": "教育培训",
            "region": "浙江",
            "total_leads": 8500,
            "valid_leads": 8200,
            "cost_per_lead": 1.2,
            "contact_rate": 0.72,
            "interest_rate": 0.18,
        },
        {
            "name": "bd-20251016-IT培训意向",
            "source": "百度",
            "industry": "职业培训",
            "region": "北京",
            "total_leads": 5000,
            "valid_leads": 4800,
            "cost_per_lead": 2.5,
            "contact_rate": 0.58,
            "interest_rate": 0.22,
        },
        {
            "name": "tt-20251017-金融理财",
            "source": "头条",
            "industry": "金融服务",
            "region": "上海",
            "total_leads": 12000,
            "valid_leads": 11500,
            "cost_per_lead": 1.8,
            "contact_rate": 0.45,
            "interest_rate": 0.12,
        },
        {
            "name": "wx-20251018-房产咨询",
            "source": "微信",
            "industry": "房地产",
            "region": "广东",
            "total_leads": 6000,
            "valid_leads": 5800,
            "cost_per_lead": 3.5,
            "contact_rate": 0.68,
            "interest_rate": 0.25,
        },
        {
            "name": "xhs-20251019-美妆护肤",
            "source": "小红书",
            "industry": "电商零售",
            "region": "四川",
            "total_leads": 15000,
            "valid_leads": 14200,
            "cost_per_lead": 0.5,
            "contact_rate": 0.78,
            "interest_rate": 0.30,
        },
        {
            "name": "dy-20251020-汽车销售",
            "source": "抖音",
            "industry": "汽车行业",
            "region": "湖北",
            "total_leads": 4500,
            "valid_leads": 4300,
            "cost_per_lead": 5.0,
            "contact_rate": 0.52,
            "interest_rate": 0.20,
        },
        {
            "name": "bd-20251021-医疗咨询",
            "source": "百度",
            "industry": "医疗健康",
            "region": "河南",
            "total_leads": 7000,
            "valid_leads": 6500,
            "cost_per_lead": 4.2,
            "contact_rate": 0.60,
            "interest_rate": 0.28,
        },
        {
            "name": "ks-20251022-家装服务",
            "source": "快手",
            "industry": "家居建材",
            "region": "山东",
            "total_leads": 9000,
            "valid_leads": 8600,
            "cost_per_lead": 1.5,
            "contact_rate": 0.70,
            "interest_rate": 0.16,
        },
        {
            "name": "tt-20251023-旅游度假",
            "source": "头条",
            "industry": "旅游服务",
            "region": "云南",
            "total_leads": 11000,
            "valid_leads": 10500,
            "cost_per_lead": 0.9,
            "contact_rate": 0.75,
            "interest_rate": 0.35,
        },
    ]
    
    packages = []
    for data in test_packages:
        # 检查是否已存在同名数据包
        existing = LeadPackage.query.filter_by(name=data["name"]).first()
        if existing:
            print(f"⚠️  数据包 '{data['name']}' 已存在，跳过")
            continue
        
        # 创建数据包
        package = LeadPackage(**data)
        
        # 计算指标
        package.calculate_metrics()
        
        # 随机设置创建时间（过去7天内）
        days_ago = random.randint(0, 7)
        package.created_at = datetime.utcnow() - timedelta(days=days_ago)
        package.updated_at = package.created_at
        
        packages.append(package)
        print(f"✅ 创建数据包: {data['name']} (线索数: {data['total_leads']})")
    
    return packages


def seed_database():
    """填充测试数据"""
    print("🚀 开始生成测试数据...")
    print("=" * 60)
    
    # 生成测试数据包
    packages = generate_test_packages()
    
    if not packages:
        print("\n⚠️  没有新数据包需要添加")
        return
    
    # 批量添加
    db.session.add_all(packages)
    
    try:
        db.session.commit()
        print("=" * 60)
        print(f"✅ 成功添加 {len(packages)} 个测试数据包！")
        print("\n📊 数据统计:")
        print(f"   总线索数: {sum(p.total_leads for p in packages):,}")
        print(f"   总成本: ¥{sum(p.total_cost for p in packages):,.2f}")
        print(f"   平均接通率: {sum(p.contact_rate for p in packages) / len(packages) * 100:.1f}%")
    except Exception as e:
        db.session.rollback()
        print(f"❌ 添加失败: {str(e)}")
        raise


def clear_test_data():
    """清除所有测试数据（谨慎使用）"""
    print("⚠️  警告：即将清除所有数据包...")
    
    count = LeadPackage.query.delete()
    db.session.commit()
    
    print(f"✅ 已清除 {count} 个数据包")


if __name__ == "__main__":
    import sys
    
    app = create_app("production")
    
    with app.app_context():
        if len(sys.argv) > 1 and sys.argv[1] == "--clear":
            # 清除数据模式
            confirm = input("确定要清除所有数据吗？(yes/no): ")
            if confirm.lower() == "yes":
                clear_test_data()
            else:
                print("已取消")
        else:
            # 生成测试数据
            seed_database()

