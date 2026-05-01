from pathlib import Path
from fastapi.staticfiles import StaticFiles
import sys
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

sys.path.append(str(Path(__file__).parent.parent))

from database.config import app1
from api.router import api_router
from core.kuayu import setup_cors

app = app1
app.include_router(api_router)
setup_cors(app)

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=os.getenv("HOST"), port=int(os.getenv("PORT")))