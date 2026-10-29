from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# CORS (Cross-Origin Resource Sharing) settings: Handle cross-origin requests (Middleware) 
app = FastAPI()

# Allow requests from any origin (for development purposes or Frontend URL)
origin = [
    "http://localhost:3000",  # React frontend URL
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World : Cors Middleware is working!"}
