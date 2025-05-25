from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db_base import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    type = Column(String)  # "User" or "Skilled Person"
    contact = Column(String)
    city = Column(String)

    # Relationships (optional, if you want)
    requests = relationship("Request", back_populates="user")


class ServiceProvider(Base):
    __tablename__ = 'providers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact = Column(String)
    skill = Column(String)


class Request(Base):
    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    service_type = Column(String)
    status = Column(String)

    user = relationship("User", back_populates="requests")
