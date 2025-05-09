"""
控制器模块初始化文件
"""
from flask import Blueprint

# 创建两个蓝图实例
m_bp = Blueprint('module_web', __name__, url_prefix="/web")
bp = Blueprint('global_web', __name__)

# 导入路由模块以确保它们被注册
from src.webserver.controllers import webcontroller, modulewebcontroller