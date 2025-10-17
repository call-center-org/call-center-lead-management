"""
通话记录模型
"""
from datetime import datetime
from app import db


class Call(db.Model):
    """通话记录表"""
    __tablename__ = 'calls'
    
    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # 外键：关联外呼任务
    task_id = db.Column(
        db.Integer,
        db.ForeignKey('dial_tasks.id', ondelete='CASCADE'),
        nullable=False,
        comment='外呼任务 ID'
    )
    
    # 通话信息
    phone_number = db.Column(db.String(20), nullable=False, comment='电话号码')
    call_time = db.Column(db.DateTime, default=datetime.utcnow, comment='拨打时间')
    duration = db.Column(db.Integer, default=0, comment='通话时长（秒）')
    
    # 通话结果
    result = db.Column(
        db.String(20),
        default='no_answer',
        comment='通话结果: connected/voicemail/busy/no_answer/rejected'
    )
    
    # 备注信息
    notes = db.Column(db.Text, comment='通话备注')
    
    # 客户信息
    customer_name = db.Column(db.String(100), comment='客户姓名')
    company = db.Column(db.String(200), comment='公司名称')
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment='更新时间'
    )
    
    # 关系：一个通话有多个标签
    tags = db.relationship(
        'CallTag',
        backref='call',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    def __repr__(self):
        return f'<Call {self.phone_number} at {self.call_time}>'
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'task_id': self.task_id,
            'phone_number': self.phone_number,
            'call_time': self.call_time.isoformat() if self.call_time else None,
            'duration': self.duration,
            'result': self.result,
            'notes': self.notes,
            'customer_name': self.customer_name,
            'company': self.company,
            'tags': [tag.to_dict() for tag in self.tags],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    @property
    def is_connected(self):
        """是否接通"""
        return self.result == 'connected'
    
    @property
    def duration_minutes(self):
        """通话时长（分钟）"""
        return round(self.duration / 60, 2)

