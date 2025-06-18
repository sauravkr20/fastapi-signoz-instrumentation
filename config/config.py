import os 
from dotenv import load_dotenv


load_dotenv()

APP_NAME= os.getenv("APP_NAME", "fastapi-otel-template")
APP_ENV= os.getenv("APP_ENV", "development")

