from fastapi import FastAPI,HTTPException,Depends,Header

#JWT Authentication Token:
from jose import JWTError, jwt

# Date and Time Manipulation:
from datetime import datetime, timedelta, timezone

#Register App
app = FastAPI()

#JWT Authentication Token: 
#   Used for secure communication between client and server. 
#   It ensures that the requests are coming from authenticated users and helps protect sensitive data.
# Package: pip install python-jose

SECRET_KEY = "Bhavya@2508"
ALGORITHM = "HS256"

#Create Access Token Function:
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    print("Expire Time:", expire)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

#Verify Access Token Function:
def verify_access_token(token: str = Header(None)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid or Expired token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")

@app.post("/login")
async def login(username: str, password: str):
    # Validate user credentials (this is just a placeholder, implement your own logic)
    if username == "admin" and password == "1234":
        access_token = create_access_token(data={"sub": username})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/secure")
def secure_data(user = Depends(verify_access_token)):
    return {"message": f"Hello, {user}. This is a secure endpoint."}
