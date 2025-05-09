"""
Web控制器模块的单元测试
"""
import pytest
from flask import Flask
import json
import ast

from src.webserver.app import create_app

# pytest fixture装饰器
# 用于创建测试夹具，提供测试客户端实例
# 每个测试用例运行前会自动调用该fixture
# 使用yield可以在测试结束后进行清理工作
@pytest.fixture
def client():
    """
    创建测试客户端
    Returns:
        FlaskClient: Flask 测试客户端实例
    """
    app = create_app()
    # 设置应用为测试模式
    # 测试模式与标准模式的区别:
    # 1. 错误处理更详细 - 会显示完整的错误堆栈
    # 2. 禁用错误捕获 - 让错误直接抛出便于测试
    # 3. 关闭请求前后的回调函数
    # 4. 提供测试专用的客户端接口
    app.config['TESTING'] = True
    # 创建测试客户端并使用上下文管理器
    with app.test_client() as client:
        # 使用yield返回客户端实例,测试完成后会自动清理
        yield client

def test_home_route(client):
    """
    测试首页路由
    """
    # 测试根路径
    response = client.get('/')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'hello world'
    
    # 测试 /web 路径
    response = client.get('/web/home_web')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'hello world'

    response = client.get('/web')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'hello world'

    # 测试 /home 路径
    response = client.get('/home')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'hello world'
    
    

def test_get_count_valid_input(client):
    """
    测试 get_count 路由的有效输入
    """
    # 测试正常输入
    response = client.get('/get_count?a=5&b=3')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == '8'

    # 测试默认值
    response = client.get('/get_count?a=5')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == '5'

    # 测试负数
    response = client.get('/get_count?a=-5&b=3')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == '-2'

def test_get_count_invalid_input(client):
    """
    测试 get_count 路由的无效输入
    """
    # 测试非数字输入
    response = client.get('/get_count?a=abc&b=3')
    assert response.status_code == 400
    assert response.data.decode('utf-8') == '错误：参数必须是整数'

    # 测试空参数
    response = client.get('/get_count?a=&b=3')
    assert response.status_code == 400
    assert response.data.decode('utf-8') == '错误：参数必须是整数'

def test_get_count_edge_cases(client):
    """
    测试 get_count 路由的边界情况
    """
    # 测试大数
    response = client.get('/get_count?a=999999999&b=1')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == '1000000000'

    # 测试零值
    response = client.get('/get_count?a=0&b=0')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == '0'

def test_submit_route(client):
    """
    测试 submit 路由的各种情况
    """
    # 测试正常 JSON 数据
    test_data = {"name": "test", "age": 18}
    response = client.post('/web/submit', 
                          json=test_data,
                          content_type='application/json')
    assert response.status_code == 200
    # 从响应中提取数据部分
    response_text = response.data.decode('utf-8')
    response_data = ast.literal_eval(response_text.replace("成功接收数据:", ""))
    assert response_data == test_data

    # 测试非 JSON 格式请求
    response = client.post('/web/submit', 
                          data="not json data",
                          content_type='text/plain')
    assert response.status_code == 400
    assert response.data.decode('utf-8') == "错误:请求Content-Type必须是application/json"

    # 测试空请求体
    response = client.post('/web/submit', 
                          json={},
                          content_type='application/json')
    assert response.status_code == 400
    assert response.data.decode('utf-8') == "错误:请求体不能为空"

    # 测试复杂数据结构
    complex_data = {
        "user": {
            "name": "test",
            "scores": [1, 2, 3],
            "info": {"age": 18, "city": "Beijing"}
        }
    }
    response = client.post('/web/submit', 
                          json=complex_data,
                          content_type='application/json')
    assert response.status_code == 200
    # 从响应中提取数据部分
    response_text = response.data.decode('utf-8')
    response_data = ast.literal_eval(response_text.replace("成功接收数据:", ""))
    assert response_data == complex_data


def test_get_params_route(client):
    """
    测试 get_params 路由的各种情况
    """
    # 测试单个参数
    response = client.get('/web/get_params?name=test')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == "name: test"

    # 测试多个参数
    response = client.get('/web/get_params?name=test&age=18&city=Beijing')
    result = response.data.decode('utf-8')
    assert response.status_code == 200
    assert "name: test" in result
    assert "age: 18" in result
    assert "city: Beijing" in result

    # 测试无参数
    response = client.get('/web/get_params')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == "没有URL参数"

    # 测试特殊字符参数
    response = client.get('/web/get_params?name=test%20user&email=test@example.com')
    result = response.data.decode('utf-8')
    assert response.status_code == 200
    assert "name: test user" in result
    assert "email: test@example.com" in result 