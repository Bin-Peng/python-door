import json

from flask import make_response, request, current_app, Blueprint

from src.webserver.repository.models.user import User
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


@m_bp.route("/update_user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """
    更新用户信息的路由处理函数
    
    Args:
        user_id (int): 用户ID，从URL路径中获取
        
    Returns:
        Response: 包含更新结果的响应
    """
    try:
        user_service = UserService()
        
        # 获取请求体数据
        if not request.is_json:
            return make_response("错误：请求Content-Type必须是application/json", 400)
            
        update_data = request.get_json()
        if not update_data:
            return make_response("错误：请求体不能为空", 400)
        
        # 记录请求信息
        current_app.logger.info(f"更新用户请求：用户ID={user_id}，更新数据={update_data}")
        
        # 确保请求中包含更新人ID
        if 'updated_by' not in update_data:
            return make_response("错误：缺少更新人ID(updated_by)", 400)
            
        updated_by = update_data.pop('updated_by')  # 从更新数据中提取更新人ID
        
        # 调用服务更新用户
        updated_user = user_service.update_user(user_id, update_data, updated_by)
        
        if updated_user:
            return make_response(f"用户 {updated_user.username} 更新成功", 200)
        else:
            return make_response(f"用户ID {user_id} 不存在", 404)
            
    except Exception as e:
        current_app.logger.error(f"更新用户异常: {str(e)}")
        return make_response(f"更新用户失败: {str(e)}", 500)


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


@m_bp.get("/get_users/<int:user_id>")
def get_users(user_id):
    user_service = UserService()
    current_app.logger.info("模块路由请求参数：用户ID=" + str(user_id))

    user = user_service.get_users(user_id)
    if user:
        # 构建用户信息字典，避免返回敏感信息如密码
        user_info = {
            "id": user[0].id,
            "username": user[0].username,
            "email": user[0].email,
            "phone": user[0].phone,
            "created_at": str(user[0].created_at)
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
