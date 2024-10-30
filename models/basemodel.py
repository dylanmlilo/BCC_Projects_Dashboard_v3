from sqlalchemy.orm import declarative_base

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
