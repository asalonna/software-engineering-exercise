from pydantic import BaseModel
from enum import Enum

class Type(str, Enum):
    question: str
    response: str

class Message(BaseModel):
    sibling_id: int
    message_type: Type
    message_body: str
    assigned_codes: int

    class Config:
        orm_mode = True

class Code(BaseModel):
    code_body: str

    class Config:
        orm_mode = True
    
class AssignedCodes(BaseModel):
    message_id: int
    code_id: int
    assigned_substring: str

    class Config:
        orm_mode = True