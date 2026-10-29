import os
from dotenv import load_dotenv

load_dotenv()

# Configuration Management: Its Help to make Application setting centralized , Data will be easy to organize
# Env:  is not a part of codebase and not pushed on github

class Settings:
    secret_key  = os.getenv("SECRET_KEY")
    db_url      = os.getenv("DB_URL")

# Class properties Assign to variable
settings = Settings()