from flask import make_response, request, current_app

from src.webserver.controllers import m_bp


@m_bp.route("/resp", methods=["GET"])
def get_resp():
    response = make_response("模块路由响应uri："+request.path)
    return response


@m_bp.before_request
def before_request():
    # 检查是否是目标路由
    current_app.logger.info("模块路由请求path："+request.path)

    if request.path == "/web/resp":
        # 检查登录参数
        if request.args.get("is_login") == "login":
            current_app.logger.debug("登录验证通过")
            return None  # 继续处理请求
        else:
            current_app.logger.debug("登录验证失败")
            return make_response("模块拦截：需要登录", 403)
    
    # 其他路由直接通过
    return None