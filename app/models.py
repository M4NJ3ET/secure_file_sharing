from sqlalchemy import Column, Integer, String, Boolean, Enum
from app.database import Base
import enum

class RoleEnum(str, enum.Enum):
    OPS = "OPS"
    CLIENT = "CLIENT"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    is_verified = Column(Boolean, default=False)
