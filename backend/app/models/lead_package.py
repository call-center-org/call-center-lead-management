"""
线索数据包模型
"""

from datetime import datetime
from app import db


class LeadPackage(db.Model):
    """线索数据包表"""

    __tablename__ = "lead_packages"

    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # 基本信息
    name = db.Column(db.String(200), nullable=False, comment="数据包名称")
    source = db.Column(db.String(100), nullable=False, comment="数据来源")
    industry = db.Column(db.String(100), comment="所属行业")
    region = db.Column(db.String(100), comment="所属地区")

    # 数据指标
    total_leads = db.Column(db.Integer, default=0, comment="线索总数")
    valid_leads = db.Column(db.Integer, default=0, comment="有效线索数")
    contact_rate = db.Column(db.Float, default=0.0, comment="接通率 (0-1)")
    interest_rate = db.Column(db.Float, default=0.0, comment="意向率 (0-1)")

    # 成本相关
    cost_per_lead = db.Column(db.Float, default=0.0, comment="单条线索成本")
    total_cost = db.Column(db.Float, default=0.0, comment="总成本")

    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="更新时间",
    )

    # 关系：一个数据包有多个外呼任务
    dial_tasks = db.relationship(
        "DialTask", backref="package", lazy="dynamic", cascade="all, delete-orphan"
    )

    # 关系：一个数据包有多个标签汇总
    tag_summaries = db.relationship(
        "PackageTagSummary",
        backref="package",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<LeadPackage {self.name}>"

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "source": self.source,
            "industry": self.industry,
            "region": self.region,
            "total_leads": self.total_leads,
            "valid_leads": self.valid_leads,
            "contact_rate": self.contact_rate,
            "interest_rate": self.interest_rate,
            "cost_per_lead": self.cost_per_lead,
            "total_cost": self.total_cost,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def calculate_metrics(self):
        """
        计算数据包指标

        接通率计算逻辑：
        - 如果有实际通话记录，从通话记录中动态计算
        - 接通率 = 接通数量 / 外呼数量
        - 接通判断：result == 'connected' 或 duration > 0
        """
        # 计算总成本
        if self.cost_per_lead > 0:
            self.total_cost = self.total_leads * self.cost_per_lead

        # 从实际通话记录计算接通率
        from app.models.call import Call

        # 获取该数据包下所有任务的所有通话记录
        total_calls = 0
        connected_calls = 0

        for task in self.dial_tasks:
            task_calls = Call.query.filter_by(task_id=task.id).all()
            total_calls += len(task_calls)

            # 统计接通数：result='connected' 或 duration > 0
            for call in task_calls:
                if call.result == "connected" or (call.duration and call.duration > 0):
                    connected_calls += 1

        # 计算接通率
        if total_calls > 0:
            self.contact_rate = connected_calls / total_calls
        else:
            # 如果没有通话记录，保持原值或默认值
            # 这适用于刚导入的历史数据，还没有实际通话
            if self.contact_rate is None or self.contact_rate == 0:
                # 可以基于有效线索数估算一个初始值
                if self.total_leads > 0:
                    self.contact_rate = min(self.valid_leads / self.total_leads, 1.0)

    def get_call_statistics(self):
        """
        获取通话统计信息（只读，不修改数据库）

        返回：
        {
            'total_calls': 外呼总数,
            'connected_calls': 接通数量,
            'contact_rate': 接通率,
            'has_call_data': 是否有通话记录
        }
        """
        from app.models.call import Call

        total_calls = 0
        connected_calls = 0

        for task in self.dial_tasks:
            task_calls = Call.query.filter_by(task_id=task.id).all()
            total_calls += len(task_calls)

            for call in task_calls:
                if call.result == "connected" or (call.duration and call.duration > 0):
                    connected_calls += 1

        contact_rate = (connected_calls / total_calls) if total_calls > 0 else 0.0

        return {
            "total_calls": total_calls,
            "connected_calls": connected_calls,
            "contact_rate": contact_rate,
            "has_call_data": total_calls > 0,
        }
