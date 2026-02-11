from fastapi import FastAPI
from tortoise import Tortoise
import sys
import os
from pathlib import Path
from fastapi.staticfiles import StaticFiles

sys.path.append(str(Path(__file__).parent.parent))

from database.config import DATABASE_CONFIG, app1
from api.router import api_router
from core.kuayu import setup_cors

app = app1
app.include_router(api_router)
setup_cors(app)


os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=1080)
