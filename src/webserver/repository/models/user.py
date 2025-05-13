from datetime import datetime
from sqlalchemy import Column, BigInteger, String, TIMESTAMP, Boolean, Table

from src.webserver.config.db_configuration import Base, engine


class User(Base):
    # __tablename__ = 'users'

    __table__ = Table("users", Base.metadata,autoload_with=engine)
    #
    # def __init__(self, username, password, email, phone, created_by, updated_by):
    #     self.username = username
    #     self.password = password
    #     self.email = email
    #     self.phone = phone
    #     self.created_by = created_by
    #     self.updated_by = updated_by
