"""
Flask 应用实例和启动逻辑
"""
from flask import Flask
from src.webserver.controllers.webcontroller import bp
def create_app():
    """
    创建并配置 Flask 应用
    Returns:
        Flask: Flask 应用实例
    """
    app = Flask(__name__)
    
    with app.app_context():
        # 注册路由
        app.register_blueprint(bp)
    
    return app

app = create_app()

def run_app():
    """
    启动 Flask 应用
    """
    print(app.url_map)
    app.run(host='127.0.0.1', port=5000)

if __name__ == "__main__":
    run_app()
