from sqlalchemy.ext.declarative import declarative_base
from models.engine.database import session

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        attrs = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        return f"{self.__class__.__name__}({attrs})"
    
    def to_dict(self):
        """Converts a SQLAlchemy model instance to a dictionary."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    

    def add_(self):
        try:
            session.add(self)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error occurred: {e}")
            raise
        finally:
            session.close()

    def update(self):
        """Commits the changes made to the current instance."""
        session.commit()

    def delete(self):
        """Deletes the current instance from the session."""
        session.delete(self)
        session.commit()
