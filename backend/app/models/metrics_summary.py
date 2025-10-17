"""
指标汇总模型
"""
from datetime import datetime, date
from app import db


class MetricsSummary(db.Model):
    """指标汇总表"""
    __tablename__ = 'metrics_summaries'
    
    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # 日期（用于按天汇总）
    date = db.Column(db.Date, nullable=False, unique=True, comment='汇总日期')
    
    # 数据包指标
    total_packages = db.Column(db.Integer, default=0, comment='数据包总数')
    new_packages = db.Column(db.Integer, default=0, comment='新增数据包数')
    total_leads = db.Column(db.Integer, default=0, comment='线索总数')
    
    # 通话指标
    total_calls = db.Column(db.Integer, default=0, comment='总拨打次数')
    connected_calls = db.Column(db.Integer, default=0, comment='接通次数')
    total_duration = db.Column(db.Integer, default=0, comment='总通话时长（秒）')
    
    # 平均指标
    avg_contact_rate = db.Column(db.Float, default=0.0, comment='平均接通率 (0-1)')
    avg_interest_rate = db.Column(db.Float, default=0.0, comment='平均意向率 (0-1)')
    avg_call_duration = db.Column(db.Integer, default=0, comment='平均通话时长（秒）')
    
    # 成本收益
    total_cost = db.Column(db.Float, default=0.0, comment='总成本')
    total_revenue = db.Column(db.Float, default=0.0, comment='总收益')
    roi = db.Column(db.Float, default=0.0, comment='投资回报率')
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment='更新时间'
    )
    
    def __repr__(self):
        return f'<MetricsSummary {self.date}>'
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date else None,
            'total_packages': self.total_packages,
            'new_packages': self.new_packages,
            'total_leads': self.total_leads,
            'total_calls': self.total_calls,
            'connected_calls': self.connected_calls,
            'total_duration': self.total_duration,
            'avg_contact_rate': self.avg_contact_rate,
            'avg_interest_rate': self.avg_interest_rate,
            'avg_call_duration': self.avg_call_duration,
            'total_cost': self.total_cost,
            'total_revenue': self.total_revenue,
            'roi': self.roi,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    @staticmethod
    def calculate_today_metrics():
        """计算今日指标"""
        from .lead_package import LeadPackage
        from .call import Call
        
        today = date.today()
        
        # 获取或创建今日汇总
        summary = MetricsSummary.query.filter_by(date=today).first()
        if not summary:
            summary = MetricsSummary(date=today)
            db.session.add(summary)
        
        # 统计数据包
        summary.total_packages = LeadPackage.query.count()
        summary.new_packages = LeadPackage.query.filter(
            db.func.date(LeadPackage.created_at) == today
        ).count()
        
        # 统计线索
        summary.total_leads = db.session.query(
            db.func.sum(LeadPackage.total_leads)
        ).scalar() or 0
        
        # 统计今日通话
        today_calls = Call.query.filter(
            db.func.date(Call.call_time) == today
        )
        summary.total_calls = today_calls.count()
        summary.connected_calls = today_calls.filter_by(result='connected').count()
        
        # 计算平均接通率
        if summary.total_calls > 0:
            summary.avg_contact_rate = summary.connected_calls / summary.total_calls
        
        # 计算平均通话时长
        summary.total_duration = db.session.query(
            db.func.sum(Call.duration)
        ).filter(
            db.func.date(Call.call_time) == today
        ).scalar() or 0
        
        if summary.connected_calls > 0:
            summary.avg_call_duration = summary.total_duration // summary.connected_calls
        
        # 计算成本
        summary.total_cost = db.session.query(
            db.func.sum(LeadPackage.total_cost)
        ).scalar() or 0.0
        
        db.session.commit()
        return summary

