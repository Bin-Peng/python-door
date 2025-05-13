"""
Flask 应用实例和启动逻辑
"""
import logging

from flask import Flask, request

from src.webserver.config.web_config import WEB_CONFIG

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def create_app():
    """
    创建并配置 Flask 应用
    Returns:
        Flask: Flask 应用实例
    """
    app = Flask(__name__)
    
    # 添加请求日志记录
    @app.before_request
    def log_request_info():
        app.logger.debug('请求路径: %s', request.path)
        app.logger.debug('请求方法: %s', request.method)
        app.logger.debug('请求参数: %s', request.args)
    
    # 添加响应日志记录
    @app.after_request
    def log_response_info(response):
        app.logger.debug('响应状态码: %s', response.status_code)
        return response
    
    with app.app_context():
        # 注册路由
        from src.webserver.controllers.module_web_controller import m_bp
        from src.webserver.controllers import bp
        app.register_blueprint(bp)
        app.register_blueprint(m_bp)
    
    return app

app = create_app() 

def run_app():
    """
    启动 Flask 应用
    """
    # 设置日志级别为DEBUG
    urlmap= "注册的url："+ app.url_map.__str__()
    logger.info(urlmap)
    logger.info("WEB的配置"+WEB_CONFIG.__str__())
    logger.info(WEB_CONFIG.get('host'))
    app.run(host=WEB_CONFIG.get('host'), port=WEB_CONFIG.get('port'))

if __name__ == "__main__":
    run_app()
