from flask import current_app
from sqlalchemy.orm import sessionmaker, scoped_session

from src.webserver.db.dbconfiguration import get_db, engine
from src.webserver.db.models.user import User

dbsession = get_db()
# 创建会话工厂
SessionLocal = sessionmaker(autoflush=True, bind=engine)
db_session = scoped_session(SessionLocal)

class UserService:
    def add_user(self, user: User):
        # 添加到数据库会话
        current_app.logger.info(f"添加用户到数据库: {user.__dict__}")
        db_session.add(user)
        db_session.commit()
        return user

    def get_user_by_id(self, user_id):
        user = dbsession.query(User).filter(User.id == user_id).first()
        return user
