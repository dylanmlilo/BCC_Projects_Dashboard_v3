from sqlalchemy import Column, Integer, String
from flask_login import UserMixin
from models.base import BaseModel
from models.engine.database import session
from werkzeug.security import generate_password_hash, check_password_hash


class Users(BaseModel, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    surname = Column(String(100))
    username = Column(String(50), unique=True)
    password = Column(String(256))
    email = Column(String(50), unique=True)
    role = Column(String(50))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
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