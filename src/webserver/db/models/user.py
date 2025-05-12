from datetime import datetime
from sqlalchemy import Column, BigInteger, String, TIMESTAMP, Boolean, Table
from src.webserver.db.dbconfiguration import Base, engine

class User(Base):
    __tablename__ = 'users'

    # 主键字段
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='用户ID')
    
    # 基本信息字段
    username = Column(String(50), unique=True, nullable=False, comment='用户名')
    password = Column(String(128), nullable=False, comment='密码(加密存储)')
    email = Column(String(100), unique=True, nullable=False, comment='邮箱')
    phone = Column(String(20), unique=True, nullable=False, comment='手机号码')
    
    # 审计字段
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now, comment='创建时间')
    created_by = Column(BigInteger, nullable=False, comment='创建人ID')
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    updated_by = Column(BigInteger, nullable=False, comment='更新人ID')
    is_deleted = Column(Boolean, nullable=False, default=False, comment='是否删除(0-未删除 1-已删除)')
    
    def __init__(self, username, password, email, phone, created_by, updated_by):
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.created_by = created_by
        self.updated_by = updated_by
