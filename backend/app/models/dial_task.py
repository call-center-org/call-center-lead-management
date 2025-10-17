"""
外呼任务模型
"""
from datetime import datetime
from app import db


class DialTask(db.Model):
    """外呼任务表"""
    __tablename__ = 'dial_tasks'
    
    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # 外键：关联数据包
    package_id = db.Column(
        db.Integer,
        db.ForeignKey('lead_packages.id', ondelete='CASCADE'),
        nullable=False,
        comment='数据包 ID'
    )
    
    # 任务信息
    task_name = db.Column(db.String(200), nullable=False, comment='任务名称')
    description = db.Column(db.Text, comment='任务描述')
    
    # 任务时间
    start_time = db.Column(db.DateTime, comment='开始时间')
    end_time = db.Column(db.DateTime, comment='结束时间')
    
    # 任务状态
    status = db.Column(
        db.String(20),
        default='pending',
        comment='任务状态: pending/in_progress/completed/cancelled'
    )
    
    # 任务指标
    total_calls = db.Column(db.Integer, default=0, comment='总拨打次数')
    connected_calls = db.Column(db.Integer, default=0, comment='接通次数')
    interested_calls = db.Column(db.Integer, default=0, comment='意向客户数')
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment='更新时间'
    )
    
    # 关系：一个任务有多个通话记录
    calls = db.relationship(
        'Call',
        backref='task',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    def __repr__(self):
        return f'<DialTask {self.task_name}>'
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'package_id': self.package_id,
            'task_name': self.task_name,
            'description': self.description,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'status': self.status,
            'total_calls': self.total_calls,
            'connected_calls': self.connected_calls,
            'interested_calls': self.interested_calls,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def calculate_metrics(self):
        """计算任务指标"""
        # 统计通话记录
        self.total_calls = self.calls.count()
        self.connected_calls = self.calls.filter_by(result='connected').count()
        
        # 统计意向客户（通过标签）
        interested = 0
        for call in self.calls:
            if any(tag.tag_name == 'interest_level' and tag.tag_value == 'high' 
                   for tag in call.tags):
                interested += 1
        self.interested_calls = interested
    
    @property
    def contact_rate(self):
        """接通率"""
        if self.total_calls == 0:
            return 0.0
        return self.connected_calls / self.total_calls
    
    @property
    def interest_rate(self):
        """意向率"""
        if self.connected_calls == 0:
            return 0.0
        return self.interested_calls / self.connected_calls

