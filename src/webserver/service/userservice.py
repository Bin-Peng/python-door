from flask import current_app
from sqlalchemy import select
from typing import List, Dict, Any

from src.webserver.config.db_configuration import get_db, db_session
from src.webserver.repository.models.user import User

dbsession =  get_db()



class UserService:
    def add_user(self, user: User):
        # 添加到数据库会话
        current_app.logger.info(f"添加用户到数据库: {user.__dict__}")
        dbsession.add(user)
        dbsession.commit()
        return user

    def get_user_by_id(self, user_id):
        user = dbsession.query(User).filter(User.id == user_id).first()
        current_app.logger.info(f"用户信息: {user.username}")
        return user


    def get_users(self, user_id):
        sql = select(User).filter_by(id=user_id)
        users = dbsession.execute(sql).scalars().all()
        for user in users:
            print(user.username)
            current_app.logger.info(f"用户信息: {user.__dict__}")
        return users

    def update_user(self, user_id, update_data, updated_by):
        """
        更新用户信息
        
        Args:
            user_id (int): 用户ID
            update_data (dict): 需要更新的用户数据字典
            updated_by (int): 更新人ID
            
        Returns:
            User: 更新后的用户对象，如果用户不存在则返回None
        """
        try:
            # 查询用户是否存在
            user = dbsession.query(User).filter(User.id == user_id).first()
            if not user:
                current_app.logger.warning(f"更新用户失败: 用户ID {user_id} 不存在")
                return None
                
            # 更新用户数据
            for key, value in update_data.items():
                if hasattr(user, key) and key != 'id':  # 防止更新主键
                    setattr(user, key, value)
            
            # 设置更新人
            user.updated_by = updated_by
            
            # 提交更新
            db_session.commit()
            current_app.logger.info(f"用户 {user_id} 更新成功")
            return user
            
        except Exception as e:
            db_session.rollback()
            current_app.logger.error(f"更新用户异常: {str(e)}")
            raise