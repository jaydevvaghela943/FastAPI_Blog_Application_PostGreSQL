from fastapi import FastAPI

# Use asyncio to run the task in the background : async/await for non-blocking operations
import asyncio

# Benefits: Performance, Scalability, Responsiveness, Resource Efficiency, Simplified Code

#Register App
app = FastAPI()

# async def task():
#     await asyncio.sleep(5)
#     return {"message": f"Task {task} completed successfully"}

@app.get("/home")
async def home():
    # Simulate a long-running task
    await asyncio.sleep(5)
    return {"message": "Task completed successfully"}