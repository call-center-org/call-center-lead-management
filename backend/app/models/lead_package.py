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
        """计算数据包指标"""
        if self.total_leads > 0:
            self.contact_rate = self.valid_leads / self.total_leads

        if self.cost_per_lead > 0:
            self.total_cost = self.total_leads * self.cost_per_lead
