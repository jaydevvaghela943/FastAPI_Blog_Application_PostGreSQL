from fastapi import FastAPI,HTTPException,Depends,Query
from database import engine,SessionLocal
import models,schemas
from sqlalchemy.orm import Session

# For Auth
from auth import create_token,verify_token

# * Blog API Project
#===========================#
# 1. PostgreSQL setup + FastAPI
# 2. CRUD APIs
# 3. JWT Auth (OAuth2)
# 4. Pagination + Search
# 5. Code Push on Github

# Packages : psycopg2-binary (For PostgreSQL)
# Create : database.py, model.py, config.py, .env, main.py

# Create table in database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# DB Dependency : check connection every time
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return{
        "message":"Blog api start"
    }

# Start Blog Application Logic

#Create Blog : + Auth or Protected Routes
@app.post("/blogs",response_model=schemas.BlogCreate)
async def create_blog(blog:schemas.BlogCreate,db:Session = Depends(get_db), user = Depends(verify_token)):
    new_blog = models.Blog(title = blog.title,content= blog.content)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

#Read all Blog : More record use : list
#@app.get("/blogs",response_model=list[schemas.BlogResponse])
#async def get_all(db:Session = Depends(get_db)):
@app.get("/blogs")
async def get_all(page:int=1, limit:int=5, search:str = Query(default=""),db:Session = Depends(get_db)):
    query = db.query(models.Blog)
    if search:
        query = query.filter(models.Blog.title.ilike(f"%{search}%"))

    total = query.count()
    skip = (page-1)*limit
    
    blogs = query.offset(skip).limit(limit).all()
    return {
        "page":page,
        "limit":limit,
        "total":total,
        "data":blogs
    }

#Read One Blog
@app.get("/blogs/{id}",response_model=schemas.BlogResponse)
async def get_one(id:int,db:Session = Depends(get_db)):
    result = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not result:
        raise HTTPException(status_code=404,detail="Record not found")
    return result

#Update Blog details
@app.put("/blogs/{id}",response_model=schemas.BlogResponse)
async def update_blog(id:int,blog:schemas.BlogCreate,db:Session = Depends(get_db)):
    result = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not result:
        raise HTTPException(status_code=404,detail="Record not found")
    
    result.title = blog.title
    result.content = blog.content
    
    db.commit()
    return result

#Delete Blog Details : Protected Route
@app.delete("/blogs/{id}")
async def delete_blog(id:int,db:Session = Depends(get_db),user = Depends(verify_token)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=404,detail="Record not found")

    blog.delete()
    db.commit()
    return {"message":"Record deleted successfully"}

#Auth Logic Start Here
@app.post("/login")
async def login():
    return {
        "access_token":create_token({"sub":"admin"}),
        "token_type":"bearer"
    }