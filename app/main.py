from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.routers import slack
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(slack.router, prefix="/slack", tags=["slack"])

@app.get("/", tags=["root"])
async def root():
    return {"app": f"{os.getenv('APP_NAME')}"}
