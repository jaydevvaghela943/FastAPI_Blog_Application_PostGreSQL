from fastapi import FastAPI

# * Create app : Register App
app = FastAPI()

# /docs  : Opens Swagger UI
# /redoc : Opens ReDoc

# ? Define simple Get Endpoint : Here @app is Decorator
@app.get("/")
def read_root():
    return {"message":"Welcome Fastapi First API"}

# ? Define simple Post Endpoint
@app.post("/greet")
def store_data(name:str,data:dict):
     return {"message":f"Your name is: {name}, Address : {data}"}
