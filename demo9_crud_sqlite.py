from fastapi import FastAPI
from fastapi import Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session,declarative_base

# ? Create app : Register App
app = FastAPI()

#Database Configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False})

# Create SessionLocal class
SessionLocal = sessionmaker(bind=engine)

# Base class for models
Base = declarative_base()

#Define Table Model
class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    completed = Column(String)

#Create tables in the database
Base.metadata.create_all(bind=engine)

# Create a dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Create API Endpoints
@app.post("/todos")
async def create_todo(title: str, db: Session = Depends(get_db)):
    todo = Todo(title=title, completed="False")
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return {"message": "Todo created successfully", "Data": todo}

# Read all todos
@app.get("/todos")
async def read_todos(db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    return {"message": "Todos retrieved successfully", "Total": len(todos), "Data": todos}

# Read a single todo by ID
@app.get("/todos/{todo_id}")
async def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo retrieved successfully", "Data": todo}


# Update a todo by ID
@app.put("/todos/{todo_id}")
async def update_todo(todo_id: int, title: str, completed: str, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo.title = title
    db.commit()
    db.refresh(todo)
    return {"message": "Todo updated successfully", "Data": todo}

#Delete a todo by ID
@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}