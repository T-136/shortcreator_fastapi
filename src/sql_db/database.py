from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time
from dotenv import load_dotenv
load_dotenv()

# SQLALCHEMY_DTABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DTABASE_URL = "postgresql://postgres:postgres@localhost:5432/creatorDBpostgresql://postgres:postgres@localhost:5432/creatorDB" 

SQLALCHEMY_DTABASE_URL = os.getenv("DOCKER_DATABASE")


engine = create_engine(
    SQLALCHEMY_DTABASE_URL
    # , connect_args={
    #     "check_same_thread": False
    # }
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
    


    
