from fastapi import FastAPI
from pydantic import BaseModel

# * Create app : Register App
app = FastAPI()

# * Define Item Model : Request Validation
class Item(BaseModel):
    name:str
    price:float


# * Temporary In-Memory Storage
items = {}

# * CREATE : POST
@app.post("/items/")
async def create_item(item:Item):
    item_id = len(items)+1
    items[item_id] = item
    return {"id":item_id,"item":item}


# * READ : GET ONE
@app.get("/items/{item_id}")
async def fetch_one(item_id:int):
    return items.get(item_id,{"error":"Item not found"})


# * READ : GET ALL
@app.get("/items/")
async def fetch_all():
    return {"message":"Fetch all data","data":items}

# * UPDATE
@app.put("/items/{item_id}")
async def update_one(item_id:int,item:Item):
    if item_id in items:
        items[item_id] = item
        return {"message":"Item updated successfully", "item":item}
    return {"error":"Item not found"}

# * DELETE
@app.delete("/items/{item_id}")
async def delete_one(item_id:int):
    if item_id in items:
        delete_item = items.pop(item_id)
        return {"message":"Item deleted successfully", "deleted_item":delete_item}
        
    return {"message":"item not found"}