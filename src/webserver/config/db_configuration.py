"""数据库配置模块"""
import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from sqlalchemy.ext.declarative import declarative_base
from logging import getLogger

from src.webserver.config import door_config

# 创建日志记录器
logger = getLogger(__name__)

# 创建基类
Base = declarative_base()

# 使用 door_config 构建数据库连接URL
DATABASE_URL = door_config.SQLALCHEMY_DATABASE_URI

# 创建数据库引擎
try:
    engine = create_engine(
        DATABASE_URL,
        echo=door_config.SQLALCHEMY_ECHO,  # 使用 door_config 的设置
        pool_size=door_config.SQLALCHEMY_POOL_SIZE,  # 连接池大小
        max_overflow=door_config.SQLALCHEMY_MAX_OVERFLOW,  # 超出连接池大小时，最多可创建的额外连接数
        pool_pre_ping=door_config.SQLALCHEMY_POOL_PRE_PING
    )
    logger.info(f"成功连接到数据库: {door_config.DB_HOST}:{door_config.DB_PORT}/{door_config.DB_DATABASE}")
except Exception as e:
    logger.error(f"数据库连接失败: {str(e)}")
    raise

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
