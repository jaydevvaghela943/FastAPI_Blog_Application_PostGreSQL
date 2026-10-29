from fastapi import FastAPI, HTTPException, Depends
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

# JWT + OAuth2 + Password Hashing + Token Expiration + Secure Endpoints : Production Ready Authentication System
app = FastAPI()

# Setup all Configurations
SECRET_KEY = "Bhavya@2508"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_MINUTES = 30

# Password Hashing Setup + OAuth2 Setup + Dummy User Data
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_setup = OAuth2PasswordBearer(tokenUrl="login")
fake_user_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("admin@123")
    }
}

# Hash Password + Verify Password
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Create Token:
async def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

# Verify Token:
async def verify_token(token: str = Depends(oauth2_setup)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid or Expired token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")


# Login Endpoint: Create Access Token
@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_user_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = await create_token({"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Check Valid Token and Access Protected Route
@app.get("/protected")
async def protected_route(username: str = Depends(verify_token)):
    return {"message": f"Hello {username}, you have access to this protected route!"}