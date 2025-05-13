"""数据库配置模块"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from sqlalchemy.ext.declarative import declarative_base
from typing import TypeVar, Type

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
SessionLocal = sessionmaker(autoflush=True, bind=engine)
# 明确指定类型为 scoped_session[Session]
db_session: scoped_session[Session] = scoped_session(SessionLocal)

def get_db() -> scoped_session[Session]:
    """
    获取数据库会话
    Returns:
        scoped_session[Session]: 数据库会话对象
    """
    try:
        return db_session
    except Exception as e:
        db_session.rollback()
        raise e
    finally:
        db_session.close()    
