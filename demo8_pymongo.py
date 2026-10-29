from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId

#https://www.geeksforgeeks.org/python/database-integration-with-fastapi/
#https://www.geeksforgeeks.org/python/fastapi-tutorial/

# ? Create app : Register App
app = FastAPI()

# Connect to MongoDB
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["user_auth"]
student_collection = db["students"]

# Pydantic Model : Request/Response Body
class Address(BaseModel):
    city: str
    country: str

class Student(BaseModel):
    name: str
    age: int
    address: Address # link to Address Model



@app.get("/")
def home():
    return {"message": "Welcome FastAPI, Workspace"}

@app.post("/students",status_code=201)
async def create_student(student: Student):
    result = student_collection.insert_one(student.model_dump())  # Use model_dump() to convert Pydantic model to dict
    return {"id": str(result.inserted_id)}


@app.get("/students",response_model=list[Student])
async def list_students(country: str = None,age: str = None):
    query = {}
    if country:
        query['address.country'] = country
    if age:
        query['age'] = {"$gte": age}

    students = list(student_collection.find(query))  # Exclude the _id field from the response
    return students

@app.get("/students/{student_id}",response_model=Student)
async def get_student(student_id: str):
    student = student_collection.find_one({"_id": ObjectId(student_id)},{"_id": 0})  # Exclude the _id field from the response
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student