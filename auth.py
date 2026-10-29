from jose import JWTError,jwt
from datetime import datetime,timedelta,timezone
from fastapi import HTTPException,Depends
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

# Config Variables
SECRET_KEY = "Bhavya@2508"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_MINUTES=30

#OAuth2 Configuration
oauth_setup = OAuth2PasswordBearer(tokenUrl="login")

#Passlib Configuration
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

#=====Start Hash | Verify password======#
def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password:str,hash_password:str):
    return pwd_context.verify(plain_password,hash_password)

#===============END=====================#

#Create Token
def create_token(data:dict):
    print("data===========",data)
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token

#Verify Token
def verify_token(token:str = Depends(oauth_setup)):
    try:
        print("token===",token)
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        print("sss=========",payload)
        print("all data===",payload.get("sub"))
        username:str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=404,detail="Invalid or Expired token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")
        
