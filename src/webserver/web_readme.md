# 使用flask初级启动web服务

### 步骤一：
* 使用Blueprint： __init__.py文件下构造bp = Blueprint('web_one', __name__)

### 步骤二：
在实际的controller中，使用bp.route()的方式注册声明路由

### 
在app.py中注册：app.register_blueprint(bp),同时注意必须要在注册前引入bp所在的controller类
