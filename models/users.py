from sqlalchemy import Column, Integer, String
from flask_login import UserMixin
from models.base import BaseModel
from models.engine.database import session


class Users(BaseModel, UserMixin):
    """
    Represents a table for users with the following columns:
    - id (Integer): The primary key of the user.
    - name (String): The name of the user.
    - username (String): The username of the user (unique).
    - password (String): The password of the user.
    - email (String): The email of the user (unique).
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    surname = Column(String(100))
    username = Column(String(50), unique=True)
    password = Column(String(50))
    email = Column(String(50), unique=True)
    role = Column(String(50))
    
    def has_role(self, role):
        return self.role == role


    @classmethod
    def user_data_to_dict_list(cls):
        try:
            users = session.query(cls).all()
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")
        return [user.to_dict() for user in users]