from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    contacts = relationship("Contact", back_populates="user")


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100))
    phone_number = Column(String(20))
    date_of_birth = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="contacts")
