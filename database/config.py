from fastapi import FastAPI
from tortoise import Tortoise
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

# 加载环境变量
load_dotenv()

# MySQL数据库配置
DATABASE_CONFIG = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": os.getenv("DB_HOST"),
                "port": int(os.getenv("DB_PORT")),
                "user": os.getenv("DB_USER"),
                "password": os.getenv("DB_PASSWORD"),
                "database": os.getenv("DB_NAME"),
            }
        }
    },
    "apps": {
        "models": {
            "models": ["models.models"],
            "default_connection": "default",
        }
    },
    'use_tz': False,
    'timezone': os.getenv("DB_TIMEZONE")
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await Tortoise.init(config=DATABASE_CONFIG)
        await Tortoise.generate_schemas()
        print("✅ 数据库连接成功")
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        raise
    yield
    await Tortoise.close_connections()

app1 = FastAPI(lifespan=lifespan)