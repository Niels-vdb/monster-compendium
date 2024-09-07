from sqlalchemy import Column, Integer, String
from .base import Base


class Users(Base):
    __tablename__ = "Users"
    user_id = Column("User_id", Integer, primary_key=True)
    name = Column("Name", String(20), nullable=False)
    password = Column("Password", String(80), nullable=False)
    role = Column("Role", Integer)
