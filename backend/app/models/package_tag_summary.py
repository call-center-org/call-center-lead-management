"""
数据包标签汇总模型
"""
from datetime import datetime
from app import db


class PackageTagSummary(db.Model):
    """数据包标签汇总表"""
    __tablename__ = 'package_tag_summaries'
    
    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # 外键：关联数据包
    package_id = db.Column(
        db.Integer,
        db.ForeignKey('lead_packages.id', ondelete='CASCADE'),
        nullable=False,
        comment='数据包 ID'
    )
    
    # 标签统计
    tag_name = db.Column(db.String(100), nullable=False, comment='标签名称')
    tag_value = db.Column(db.String(200), comment='标签值')
    tag_count = db.Column(db.Integer, default=0, comment='标签出现次数')
    
    # 百分比
    percentage = db.Column(db.Float, default=0.0, comment='占比 (0-1)')
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment='更新时间'
    )
    
    # 唯一约束：同一数据包的同一标签名称和值只能有一条记录
    __table_args__ = (
        db.UniqueConstraint('package_id', 'tag_name', 'tag_value', name='uix_package_tag'),
    )
    
    def __repr__(self):
        return f'<PackageTagSummary {self.tag_name}: {self.tag_value} ({self.tag_count})>'
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'package_id': self.package_id,
            'tag_name': self.tag_name,
            'tag_value': self.tag_value,
            'tag_count': self.tag_count,
            'percentage': self.percentage,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

