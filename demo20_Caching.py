from fastapi import FastAPI,HTTPException
import requests
from bs4 import BeautifulSoup
import time

# Environment Variables 
app = FastAPI()

# FastAPI Tutorial #31 | Rate limiting : Protect unnessary access per route
#Package : slowapi
cache_data = []
last_fetch = 0

@app.get("/news")
async def caching():
    global cache_data, last_fetch
    start = time.time()
    print(time.time(),"====",last_fetch,"====>>",time.time() - last_fetch)
    if time.time() - last_fetch >60:
        print("Fetching fresh data")

        url="https://indianexpress.com/"
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=404,detail="No record found")

        soup = BeautifulSoup(response.text,"html.parser")
        cache_data = [item.text for item in soup.find_all("a",class_="topblockNews__sidebarLink")]
        last_fetch = time.time()
    else:
        print("Using Cache Data")

    end = time.time()
    time_taken = round(end-start,4)
    return {
        "taken_time":time_taken,
        "data":cache_data
    }