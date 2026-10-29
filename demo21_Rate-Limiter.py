from fastapi import FastAPI,HTTPException,Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

# Environment Variables 
app = FastAPI()

#Rate Limit : Slowapi : Use for security | Block UnAuthorised access

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Register limiter with FastAPI
app.state.limiter = limiter

#Error Handle
@app.exception_handler(RateLimitExceeded)
def rate_limit_handle(request:Request,exc=RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "detail":"Too many bad requests"
        }
    )


@app.get("/rate-limit")
@limiter.limit("5/minute")
async def rate_limiter(request: Request):
    return {"message":"Success: Rate Limiter"}