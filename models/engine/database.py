from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.basemodel import Base
from dotenv import load_dotenv
import os

load_dotenv()

db_connection_string = os.getenv('db_connection_string')

engine = create_engine(db_connection_string, pool_recycle=3600, pool_pre_ping=True)

Session = (sessionmaker(bind=engine))

session = Session()

Base.metadata.create_all(engine)