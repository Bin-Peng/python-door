#使用方式在其他文件中导入
#from webserver.db.dbconfiguration import Base, get_db

"""数据库配置模块"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

# 创建基类
Base = declarative_base()

# 数据库连接配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root',  # 请在实际使用时设置密码
    'database': 'python_door'
}

# 构建数据库连接URL
DATABASE_URL = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

# 创建数据库引擎
engine = create_engine(
    DATABASE_URL,
    echo=True,  # 设置为True以查看SQL语句
    pool_size=5,  # 连接池大小
    max_overflow=10  # 超出连接池大小时，最多可创建的额外连接数
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=True, autoflush=True, bind=engine)
db_session = scoped_session(SessionLocal)

def get_db():
    """获取数据库会话"""
    db = db_session
    try:
        # 使用yield返回数据库会话对象
        # yield语句会创建一个生成器,允许在with语句中使用数据库会话
        # 当with语句结束时,会自动调用生成器的close方法,确保数据库连接被正确关闭
        yield db
    finally:
        db.close()
