import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db
from fastapi.middleware.cors import CORSMiddleware

from schema import Type as SchemaType

from schema import Message as SchemaMessage

from schema import Code as SchemaCode

from schema import AssignedCodes as SchemeAssignedCodes

from models import Type as ModelType
from models import Message as ModelMessage
from models import Code as ModelCode
from models import AssignedCodes as ModelAssignedCodes

import os
from dotenv import load_dotenv

from typing import List

load_dotenv('.env')

app = FastAPI()
#todo: try catch?

#to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#to delete table data
#    db.session.query(ModelMessage).delete()
#    db.session.commit()

#fetch all messages
@app.get("/api/messages")
async def fetch_messages():
    messages = db.session.query(ModelMessage).all()
    if messages == []:
        db_msg = ModelMessage(message_type=ModelType.question, message_body="How are you feeling right now?")
        db.session.add(db_msg)
        db_msg = ModelMessage(message_type=ModelType.response, message_body="I feel scared and hopeless about my exams tomorrow")
        db.session.add(db_msg)
        db.session.commit()
        messages = db.session.query(ModelMessage).all()
    for message in messages:
        codes = ""
        assigned_codes = db.session.query(ModelAssignedCodes).filter_by(message_id=message.id)
        for assigned_code in assigned_codes:
            code_list = db.session.query(ModelCode).filter_by(id=assigned_code.code_id)
            for code in code_list:
                codes = codes + (code.code_body) + ", "
        message.code_string = codes
    return messages
    

#fetch all codes
@app.get("/api/codes")
async def fetch_codes():
    codes = db.session.query(ModelCode).all()
    if codes == []:
        db_msg = ModelCode(code_body="Stress")
        db.session.add(db_msg)
        db_msg = ModelCode(code_body="Depression")
        db.session.add(db_msg)
        db_msg = ModelCode(code_body="Anxiety")
        db.session.add(db_msg)
        db.session.commit()
        codes = db.session.query(ModelCode).all()
    return codes

#fetch specific message
@app.get("/api/messages/{id}")
async def fetch_specific_message(id: int):
    print(id)
    message = db.session.query(ModelMessage).get(id)
    codes = ""
    assigned_codes = db.session.query(ModelAssignedCodes).filter_by(message_id=message.id)
    for assigned_code in assigned_codes:
        code_list = db.session.query(ModelCode).filter_by(id=assigned_code.code_id)
        for code in code_list:
            codes = codes + (code.code_body) + ", "
    message.code_string = codes

    return message

#assign code to a message
@app.post("/api/assign_codes")
async def assign_codes(assigned: SchemeAssignedCodes):
    exists = db.session.query(ModelAssignedCodes).filter_by(code_id=assigned.code_id, message_id=assigned.message_id, assigned_substring=assigned.assigned_substring)
    for i in exists:
        return {}
    db_assigned = ModelAssignedCodes(message_id=assigned.message_id, code_id = assigned.code_id, assigned_substring = assigned.assigned_substring)
    db.session.add(db_assigned)
    db.session.commit()
    return db_assigned

#fetch assigned codes for a given message
@app.get("/api/assigned/{msg_id}")
async def fetch_assigned(msg_id: int):
    message = db.session.query(ModelMessage).get(msg_id)
    if message is None:
        return {}
    assigned_codes = db.session.query(ModelAssignedCodes).filter_by(message_id=message.id)
    if assigned_codes == []:
        return {}
    data = []
    for assigned in assigned_codes:
        data.append({
            "assigned_id": assigned.assigned_id,
            "assigned_substring": assigned.assigned_substring, 
            "code_body": assigned.code.code_body
            })
    return data


#todo: add api to delete a specified assigned code
@app.delete("/api/delete_assigned/{assigned_id}")
async def remove_code_from_message(assigned_id: int):
    db.session.query(ModelAssignedCodes).filter_by(assigned_id=assigned_id).delete()
    db.session.commit()

#for running locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)