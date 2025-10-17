"""
Flask 应用工厂函数
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import get_config

# 初始化扩展（不绑定到具体应用）
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_name=None):
    """
    应用工厂函数

    Args:
        config_name: 配置名称 ('development', 'testing', 'production')

    Returns:
        Flask 应用实例
    """
    app = Flask(__name__)

    # 加载配置
    config_class = get_config(config_name)
    app.config.from_object(config_class)

    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # 配置 CORS
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": app.config["CORS_ORIGINS"],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
            }
        },
    )

    # 注册蓝图
    register_blueprints(app)

    # 注册错误处理
    register_error_handlers(app)

    # 注册 CLI 命令
    register_commands(app)

    # 自动创建数据库表（生产环境）
    with app.app_context():
        db.create_all()

    return app


def register_blueprints(app):
    """注册蓝图"""
    from app.routes import auth_bp, packages_bp, tasks_bp, metrics_bp, data_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(packages_bp, url_prefix="/api/packages")
    app.register_blueprint(tasks_bp, url_prefix="/api/tasks")
    app.register_blueprint(metrics_bp, url_prefix="/api/metrics")
    app.register_blueprint(data_bp, url_prefix="/api/data")


def register_error_handlers(app):
    """注册错误处理器"""
    from flask import jsonify

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not Found", "message": str(error)}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({"error": "Internal Server Error", "message": str(error)}), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad Request", "message": str(error)}), 400


def register_commands(app):
    """注册自定义 CLI 命令"""

    @app.cli.command()
    def init_db():
        """初始化数据库"""
        db.create_all()
        print("✅ 数据库表创建成功！")

    @app.cli.command()
    def seed_db():
        """填充测试数据"""
        from app.models import LeadPackage

        # 创建示例数据
        package = LeadPackage(
            name="测试数据包",
            source="示例来源",
            industry="科技",
            region="江苏",
            total_leads=1000,
            valid_leads=900,
        )
        db.session.add(package)
        db.session.commit()

        print("✅ 测试数据添加成功！")
