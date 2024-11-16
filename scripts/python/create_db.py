import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from server.models import Base


db_path = "instance/"
# Creates instance folder if non exist
if not os.path.exists(db_path):
    os.makedirs(db_path)

# Creates database
db_url = f"sqlite:///{db_path}database.db"
engine = create_engine(db_url, connect_args={"check_same_thread": False})

# Creates tables
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
