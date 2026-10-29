from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# * For HTML Response Render 
from fastapi.responses import HTMLResponse


# * Create app : Register App
app = FastAPI()

#Load Template and Static Folder
app.mount("/static",StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# * Sample HTML Page
@app.get("/",response_class=HTMLResponse)
async def read_root(request:Request):
    return templates.TemplateResponse(request,"index.html",{"message":"hello"})