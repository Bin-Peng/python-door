"""
这是一个基于Flask的Web控制器模块。
主要提供了Web服务的路由处理功能，包括首页和计数接口。
"""
from flask import request

from src.webserver.controllers import bp
from src.webserver.controllers.modulewebcontroller import m_bp


@bp.route('/')
@bp.route('/home')
@m_bp.route('/home_web')
@m_bp.route('')
def home():
    """
    首页路由处理函数
    Returns:
        str: 返回一个字符串，包含'hello world'
    """
    return 'hello world'


@bp.route('/get_count')
def get_count():
    """
    获取计数路由处理函数
    从请求参数中获取 a 和 b 两个整数，返回它们的和
    Returns:
        str: 返回两个参数的和
    Raises:
        ValueError: 当参数不是有效的整数时抛出
    使用示例：
    正确请求：/get_count?a=5&b=3 将返回 "8"
    错误请求：/get_count?a=abc&b=3 将返回错误信息
    缺少参数：/get_count?a=5 将使用默认值 0 作为 b 的值
    """
    try:
        #request.args 是url上的入参
        a = int(request.args.get('a', 0))
        b = int(request.args.get('b', 0))
        return str(a + b)
    except ValueError:
        return "错误：参数必须是整数", 400


@m_bp.route('/submit', methods=['POST'])
def submit():
    """
    处理POST请求的路由函数
    从请求体中获取数据并处理
    Returns:
        str: 返回处理结果
    """
    if not request.is_json:
        return "错误:请求Content-Type必须是application/json", 400
        
    data = request.get_json()
    if not data:
        return "错误:请求体不能为空", 400
        
    return f"成功接收数据:{data}"


@m_bp.route('/get_params')
def get_params():
    """
    获取URL参数的路由处理函数
    从请求中获取所有URL参数并返回
    Returns:
        str: 返回包含所有URL参数的字符串
    使用示例:
    /get_params?name=test&age=18 将返回所有参数键值对
    """
    # 获取所有URL参数
    params = request.args
    if not params:
        return "没有URL参数"
    
    # 构建参数字符串
    result = []
    for key, value in params.items():
        result.append(f"{key}: {value}")
    
    return "\n".join(result)

