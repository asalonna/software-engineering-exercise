from typing import Union

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/messages/{message_id}")
def serve_example_message(message_id: int):
    return {"message_id": message_id}