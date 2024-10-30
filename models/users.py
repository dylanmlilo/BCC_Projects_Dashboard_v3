from sqlalchemy import Column, Integer, String
from flask_login import UserMixin
from models.basemodel import BaseModel
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
        """Hash and set the password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the hashed password."""
        return check_password_hash(self.password, password)
    
    def has_role(self, role):
        """Check if the user has the specified role."""
        return self.role == role

    @classmethod
    def user_data_to_dict_list(cls):
        """Retrieve all users and convert them to a list of dictionaries."""
        try:
            users = session.query(cls).all()
            return [user.to_dict() for user in users]
        except Exception as e:
            print(f"An error occurred: {e}")
            session.rollback()
            return []
        finally:
            session.close()