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
        print(message.id)
        assigned_codes = db.session.query(ModelAssignedCodes).filter_by(message_id=message.id)
        for assigned_code in assigned_codes:
            code_list = db.session.query(ModelCode).filter_by(id=assigned_code.code_id)
            for code in code_list:
                codes = codes + (code.code_body) + ", "
        print(codes)
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
@app.get("api/messages/{id}")
async def fetch_specific_message():
    print(1)

#assign code to a message
@app.post("/api/assign_codes")
async def assign_codes(assigned: SchemeAssignedCodes):
    db_assigned = ModelAssignedCodes(message_id=assigned.message_id, code_id = assigned.code_id, assigned_substring = assigned.assigned_substring)
    db.session.add(db_assigned)
    db.session.commit()
    return db_assigned

#fetch stuff
@app.get("/api/stuff")
async def fetch_stuff():
    stuff = db.session.query(ModelAssignedCodes).all()
    return stuff


#todo: add api to delete a specified assigned code

#fetch message codes
@app.get("api/assigned_data")
async def fetch_assigned_data():
    print(1)

#for running locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)