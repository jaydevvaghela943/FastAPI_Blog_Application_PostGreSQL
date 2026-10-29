from fastapi import FastAPI,HTTPException
import requests

# Environment Variables 
app = FastAPI()


@app.get("/posts")
async def home():
    response  = requests.get("https://jsonplaceholder.typicode.com/posts")
    data = response.json()
    return {"message": "Third party API Call","data":data}

@app.get("/posts/{id}")
async def get_one(id:int):
    response  = requests.get(f"https://jsonplaceholder.typicode.com/posts/{id}")
    if response.status_code != 200:
        raise HTTPException(status_code=404,detail="Record not found")
    
    data = response.json()
    return {"message": "Third party API Call - One Data","data":data}