"""
这是一个基于Flask的Web控制器模块。
主要提供了Web服务的路由处理功能，包括首页和计数接口。
"""
from flask import request

from src.webserver.controllers import bp


@bp.route('/')
@bp.route('/home')
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
        a = int(request.args.get('a', 0))
        b = int(request.args.get('b', 0))
        return str(a + b)
    except ValueError:
        return "错误：参数必须是整数", 400
