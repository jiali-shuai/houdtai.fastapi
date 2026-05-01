from datetime import datetime, timedelta
from typing import Optional
import jwt
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 配置项从环境变量获取
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

class TokenData:
    def __init__(self, user_id: str, exp: Optional[str] = None):
        self.user_id = user_id
        self.exp = exp

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_and_get_token_data(token: str):
    if not token:
        return {"resultCode": 401, "message": "未登录", "data": None}
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if datetime.utcnow() > datetime.fromtimestamp(payload['exp']):
            return {"resultCode": 401, "message": "token已过期", "data": None}
        user_id = payload.get("sub")
        if user_id is None:
            return {"resultCode": 401, "message": "未登录", "data": None}
        token_data = TokenData(user_id=user_id)
        return {"resultCode": 200, "message": "成功", "data": token_data}
    except jwt.PyJWTError:
        return {"resultCode": 401, "message": "未登录", "data": None}