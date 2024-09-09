from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from server.database.models import Base

db_url = "sqlite:///server/database/instance/database.db"
engine = create_engine(db_url)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()
