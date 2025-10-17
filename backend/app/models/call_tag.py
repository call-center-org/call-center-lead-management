"""
通话标签模型
"""

from datetime import datetime
from app import db


class CallTag(db.Model):
    """通话标签表"""

    __tablename__ = "call_tags"

    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # 外键：关联通话记录
    call_id = db.Column(
        db.Integer,
        db.ForeignKey("calls.id", ondelete="CASCADE"),
        nullable=False,
        comment="通话记录 ID",
    )

    # 标签信息
    tag_name = db.Column(db.String(100), nullable=False, comment="标签名称")
    tag_value = db.Column(db.String(200), comment="标签值")
    tag_type = db.Column(
        db.String(50),
        default="custom",
        comment="标签类型: interest_level/industry/follow_up/custom",
    )

    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment="创建时间")

    def __repr__(self):
        return f"<CallTag {self.tag_name}: {self.tag_value}>"

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "call_id": self.call_id,
            "tag_name": self.tag_name,
            "tag_value": self.tag_value,
            "tag_type": self.tag_type,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
