import json

from flask import make_response, request, current_app, Blueprint

from src.webserver.db.models.user import User
from src.webserver.service.userservice import UserService

# 定义全局变量用于URL前缀和路径匹配
m_web = "/web"

m_bp = Blueprint('module_web', __name__, url_prefix=m_web)


@m_bp.route("/resp", methods=["GET"])
def get_resp():
    response = make_response("模块路由响应uri：" + request.path)
    return response


@m_bp.route("/add_user", methods=["POST"])
def add_user():
    user_service = UserService()
    body = request.data  # 获取请求体数据
    user = json.loads(body)
    current_app.logger.info("模块路由请求参数：" + str(user))
    user_dict={
        "username": user["username"],
        "password": user["password"],
        "email": user["email"],
        "phone": user["phone"],
        "created_by": user["created_by"],
        "updated_by": user["updated_by"],
    }
    user_data = User(**user_dict)
    user_result=user_service.add_user(user_data)
    resp = make_response("添加用户成功,用户id"+user_result.username)
    return resp


@m_bp.route("/get_user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user_service = UserService()
    current_app.logger.info("模块路由请求参数：用户ID=" + str(user_id))

    user = user_service.get_user_by_id(user_id)
    if user:
        # 构建用户信息字典，避免返回敏感信息如密码
        user_info = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "created_at": str(user.created_at)
        }
        return user_info
    else:
        return make_response("未找到用户", 404)


@m_bp.before_request
def before_request():
    # 检查是否是目标路由
    current_app.logger.info("模块路由请求path：" + request.path)

    if request.path == (m_web + "/resp"):
        # 检查登录参数
        if request.args.get("is_login") == "login":
            current_app.logger.debug("登录验证通过")
            return None  # 继续处理请求
        else:
            current_app.logger.debug("登录验证失败")
            return make_response("模块拦截：需要登录", 403)

    # 其他路由直接通过
    return None
