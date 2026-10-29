from fastapi import FastAPI,HTTPException
import requests
from bs4 import BeautifulSoup

# Environment Variables 
app = FastAPI()

# Web Crawling | Scraping | BeautifulSoup | Pagination
# Package : BeautifulSoup4

@app.get("/news")
async def scraping(page:int =1,limit:int =5):
    url="https://indianexpress.com/"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=404,detail="No record found")

    soup = BeautifulSoup(response.text,"html.parser")
    title = []
    for item in soup.find_all("a",class_="topblockNews__sidebarLink"):
        title.append(item.text)

    # Pagination Logic
    start = (page-1)*limit
    end   = start+limit
    return {
        "message":"success",
        "page":page,
        "limit":limit,
        "total":len(title),
        "data":title[start:end]
    }
    