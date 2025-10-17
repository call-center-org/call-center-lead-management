"""
API 路由蓝图
"""

from .auth import auth_bp
from .packages import packages_bp
from .tasks import tasks_bp
from .metrics import metrics_bp
from .data import data_bp

__all__ = ["auth_bp", "packages_bp", "tasks_bp", "metrics_bp", "data_bp"]
