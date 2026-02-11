from fastapi import FastAPI, APIRouter

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from api import login, goods,order,user,image
app = FastAPI()

from fastapi import APIRouter


api_router = APIRouter(prefix="")  # 修改prefix为/api
api_router.include_router(login.router, tags=["登录"])
api_router.include_router(goods.router, tags=["商品"])
api_router.include_router(order.router, tags=["订单"])
api_router.include_router(user.router, tags=["用户"])
api_router.include_router(image.router, tags=["图片"])






app.include_router(api_router)