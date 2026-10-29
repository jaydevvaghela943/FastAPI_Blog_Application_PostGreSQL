from fastapi import FastAPI

# 1. Cors : Middleware : default middleware
from fastapi.middleware.cors import CORSMiddleware

# 2. GZipMiddleware (Response Compression) : compresses responses before sending to client mini-1000 bytes
from fastapi.middleware.gzip import GZipMiddleware

# 3. TrustedHostMiddleware - Restrict Allowed Hosts
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# 4. HTTPSRedirectMiddleware (Force HTTPS)
#from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

# * Create app : Register App
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins =["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# GZipMiddleware (Response Compression) : >1000 byte it compress before send to client
app.add_middleware(GZipMiddleware,minimum_size=1000)

# Trusted Host Middleware
app.add_middleware(TrustedHostMiddleware,allowed_hosts = ["example.com", "localhost","localhost:8000"])

# Redirect HTTP -> HTTPS
#app.add_middleware(HTTPSRedirectMiddleware)

# If any where stuck than remove pycache folder cache files

@app.get("/")
def home():
    return {"message": "CORS enabled!"}

@app.get("/large-data")
def large_data():
    return {"data":"x"*1500}

@app.get("/trusted-host")
def home2():
    return {"message": "Only trusted hosts can access this!"}

@app.get("/redirect-https")
def home3():
    return {"message": "You are redirected to HTTPS!"}
