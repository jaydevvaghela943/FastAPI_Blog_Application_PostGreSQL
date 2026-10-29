from fastapi import FastAPI,HTTPException,Request
from fastapi.responses import JSONResponse

# Environment Variables 
app = FastAPI()
# * Deploy Project on Render.com
# * Make python serup with Virtual Environment
# * Activate Environment : venv->script | Bin->activate
# * Install packages required
# * Create "requirements.txt" : pip freeze > requirements.txt (all package added in file)
# * Code Sample API in FastAPI
# * Create .env file
# * .gitignore create (exclude venv,.env, __pyCache__)
# * Create Git Repo and Push Code
# Open www.render.com => New Project => Web Services => Public Git Repository => Add Git Repo URL from Github => Connect =>
# Check : Build Command => Python Version
# Add Start Command : uvicorn main:app --host 0.0.0.0 --port 10000 > Select Free => Click on Deploy
# Application Success : Now Application will be Live