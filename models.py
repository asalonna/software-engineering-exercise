import enum
from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Type(enum.Enum):
    question = "Question"
    response = "Response"

class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True, index=True)
    sibling_id=Column(Integer, ForeignKey('Message.id'))
    message_type = Column(Type)
    message_body= Column(String)

class Code(Base):
    __tablename__ = 'code'
    id = Column(Integer, primary_key=True, index=True)
    code_body = Column(String)

class AssignedCodes(Base):
    __tablename__ = 'assigned codes'
    assigned_id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey('Message.id'))
    code_id = Column(Integer, ForeignKey('Code.id'))
    assigned_substring = Column(String)