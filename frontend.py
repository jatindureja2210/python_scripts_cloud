from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Temporary in-memory storage
store = {}

# Request model
class KeyValue(BaseModel):
    key: str
    value: str

# POST API to save key-value
@app.post("/store")
def store_data(data: KeyValue):
    store[data.key] = data.value
    return {"message": "Stored successfully", "data": store}

# GET API to view all data
@app.get("/data")
def get_data():
    return store