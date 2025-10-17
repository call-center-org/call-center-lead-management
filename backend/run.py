"""
Flask 应用启动文件
"""
import os
from app import create_app

# 获取环境配置
env = os.getenv('FLASK_ENV', 'development')
app = create_app(env)

if __name__ == '__main__':
    # 开发环境配置
    port = int(os.getenv('PORT', 5002))
    debug = env == 'development'
    
    print(f"🚀 启动 Flask 应用...")
    print(f"   环境: {env}")
    print(f"   端口: {port}")
    print(f"   调试模式: {debug}")
    print(f"   访问地址: http://localhost:{port}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )

