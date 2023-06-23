import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

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

load_dotenv('.env')

app = FastAPI()

#to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])

#fetch all messages
@app.get("/messages")
async def fetch_messages():
    messages = db.session.query(ModelMessage).all()
    return messages

#fetch all codes
@app.get("/codes")
async def fetch_codes():
    codes = db.session.query(ModelCode).all()
    return codes

#assign code to a message
@app.post("/assign_codes")
async def assign_codes(assigned: SchemeAssignedCodes):
    db_assigned = ModelAssignedCodes(message_id=assigned.message_id, code_id = assigned.code_id, assigned_substring = assigned.assigned_substring)
    db.session.add(db_assigned)
    db.session.commit()
    return db_assigned

#todo: add api to delete a specified assigned code

#for running locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)