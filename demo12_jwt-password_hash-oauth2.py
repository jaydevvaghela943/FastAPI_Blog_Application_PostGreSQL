from fastapi import FastAPI,HTTPException,Depends

#JWT Authentication Token:
from jose import JWTError, jwt

# Date and Time Manipulation:
from datetime import datetime, timedelta, timezone

# OAuth2
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Password Hashing
from passlib.context import CryptContext

#Register App
app = FastAPI()

# Production Ready Authentication System
#==============================================
# OAuth2 + JWT + Password Hashing + Token Expiration + Secure Endpoints : Production Ready Authentication System
# Package: pip install "python-jose" "passlib[bcrypt]" "python-multipart"
# pip install fastapi uvicorn passlib==1.7.4 bcrypt==4.0.1 : (Version 1.7.4 of passlib is compatible with bcrypt version 4.0.1)
# OAuth2: Is a Authorization framework which provide token based authorization.
# Password Hashing: Is a process of converting plain text password into a hashed format for secure storage.
# JWT: Used for User Authentication and Build Secure API
# OAuth2PasswordBearer : Extracts the token from the Authorization header and verifies it.

# JWT Configuration
SECRET_KEY = "Bhavya@2508"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_MINUTES=30

# Password Hashing Setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#OAuth2 Setup
oauth2_setup = OAuth2PasswordBearer(tokenUrl="login")

#Dummy User Data
fake_user_db = {
    "admin":{
        "username":"admin",
        "hashed_password": pwd_context.hash("1234")
    }
}

#Hash Password
def hash_password(password:str):
    return pwd_context.hash(password)

#Verify Password
def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)


#Create Access Token Function:
def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    print("Expire Time:", expire)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

#OAuth2 + JWT + Password Hash
@app.post("/login")
async def login(form_data:OAuth2PasswordRequestForm = Depends()):
    user = fake_user_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = create_token({"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


#Verify Access Token Function:
def verify_access_token(token: str = Depends(oauth2_setup)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid or Expired token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")
    

@app.get("/protected")
def protected_route(user = Depends(verify_access_token)):
    return {"message": f"Hello, {user}. This is a secure endpoint.(OAuth2_JWT_PASSWORD-HASHING)","data":user}
