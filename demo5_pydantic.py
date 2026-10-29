from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List

# * Create app : Register App
app = FastAPI()


# Base Model Class
class Book(BaseModel):
    title:str
    author:str
    publication_year:int
    ISBN:str

# Store Data In Temporary Memory
book_database = []

# * Create Book : POST
@app.post("/books/",response_model=Book)
async def create_book(book:Book):
    #Add data into book list
    book_database.append(book)
    return book

# * Get ALL Books : GET
@app.get("/books/",response_model=List[Book])
async def book_list():
    return book_database

# * Get One Book : GET
@app.get("/books/{isbn}",response_model=Book)
async def get_one_book(isbn:str):
    #Search Specific ISBN book
    book = next((b for b in book_database if b.ISBN == isbn),None)
    if book is None:
        raise HTTPException(status_code = 404,detail="Book not found")
    
    return book

# * Update One Book : PUT
@app.put("/books/{isbn}",response_model=Book)
async def update_book(isbn:str,update_book:Book):
    #search for specific ISBN record
    book = next((b for b in book_database if b.ISBN == isbn),None)
    if book is None:
        raise HTTPException(status_code = 404, detail="Book record not found")
    
    # Update Json
    for field in update_book.dict(exclude_unset=True):
        setattr(book,field,getattr(update_book,field))
    
    #return updated record
    return book

# * Delete Book : DELETE
@app.delete("/books/{isbn}",response_model=Book)
async def delete_book(isbn:str):
    #search Specific book
    book = next((b for b in book_database if b.ISBN == isbn), None)
    if book is None:
        raise HTTPException(status_code = 404, detail="Book record not found")
    
    book_database.remove(book)
    return book