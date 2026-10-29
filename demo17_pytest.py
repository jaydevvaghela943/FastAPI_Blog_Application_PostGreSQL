from fastapi import FastAPI

# Environment Variables 
app = FastAPI()

# Pytest : API Testing like Unit Testing
# Packages : pytest and httpx2

@app.get("/")
async def home():
    return {"message": "Hello World - Pytest"}

@app.get("/add")
def add(a:int,b:int):
    return {"result":a+b}