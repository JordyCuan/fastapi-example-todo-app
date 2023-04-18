from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    phone_number = Column(String, nullable=True)

    todos = relationship("Todo", back_populates="owner")
    address = relationship("Address", back_populates="user_address")

    address_id = Column(Integer, ForeignKey("address.id"), nullable=True)


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)

    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="todos")


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, index=True)
    address1 = Column(String, nullable=False)
    address2 = Column(String, nullable=True)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)

    user_address = relationship("User", back_populates="address")
