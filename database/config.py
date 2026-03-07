from fastapi import FastAPI
from tortoise import Tortoise
from contextlib import asynccontextmanager
from fastapi import HTTPException


import sys

from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from models.models import Admin


# MySQL数据库配置
# 修改数据库配置
DATABASE_CONFIG = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": "127.0.0.1",
                "port": 3306,
                "user": "root",
                "password": "yourpassword",
                "database": "uer",
            }
        }
    },
    "apps": {
        "models": {  # 确保app名称与模型引用一致
            "models": ["models.models"],  # 确保路径正确
            "default_connection": "default",
        }
    },
    'use_tz': False,
    'timezone': 'Asia/Shanghai'
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await Tortoise.init(config=DATABASE_CONFIG)
        await Tortoise.generate_schemas()  # 添加这行自动生成表
        print("✅ 数据库连接成功")
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        raise
    yield
    # 关闭时断开连接
    await Tortoise.close_connections()
app1 = FastAPI(lifespan=lifespan)  # 添加lifespan参数