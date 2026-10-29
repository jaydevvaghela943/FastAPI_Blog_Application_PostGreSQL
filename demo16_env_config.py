from fastapi import FastAPI
# import os
# from dotenv import load_dotenv

# This Prod configuration settings
from config import settings

# Environment Variables 
app = FastAPI()

# Load environment variables from .env file
#load_dotenv()

# For larger applications, you can use a configuration management library like Pydantic or Dynaconf to manage environment variables more effectively.
# Like config.py

@app.get("/")
async def root():
    return{
            "message": "Hello World ENV",
            "SECRET_KEY": settings.secret_key,
            "DB_URL": settings.db_url
        }
