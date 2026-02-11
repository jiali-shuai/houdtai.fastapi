
from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, status
from pydantic import BaseModel

# 配置项
SECRET_KEY = "sdassfhaf46564afag"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60



class TokenData(BaseModel):
    user_id: str
    exp: Optional[str] = None
    
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    # 复制传入的data字典
    to_encode = data.copy()
    # 如果传入的expires_delta参数不为空，则设置过期时间为当前时间加上expires_delta
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    # 否则，设置过期时间为当前时间加上ACCESS_TOKEN_EXPIRE_MINUTES
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # 将过期时间添加到to_encode字典中
    to_encode.update({"exp": expire})
    # 使用SECRET_KEY和ALGORITHM对to_encode进行编码，生成JWT
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # 返回生成的JWT
    return encoded_jwt

def verify_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    
    if not token or not isinstance(token, str):
        raise credentials_exception
        
    try:
        # 使用SECRET_KEY和ALGORITHM对token进行解码
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # 从payload中获取user_id
        user_id: str = payload.get("sub")
        # 如果user_id不存在，抛出credentials_exception
        if user_id is None:
            raise credentials_exception
        # 创建一个TokenData对象，包含user_id
        token_data = TokenData(user_id=user_id)
    except jwt.PyJWTError:
        # 如果解码失败，抛出credentials_exception
        raise credentials_exception
    # 返回TokenData对象
    return token_data

def verify_and_get_token_data(token: str):
    """
    验证token并返回统一格式的响应
    
    参数:
        token: JWT token字符串
    
    返回:
        字典格式的响应数据
    """
    if not token:
        return {"resultCode": 401, "message": "未登录", "data": None}
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if datetime.utcnow() > datetime.fromtimestamp(payload['exp']):
            return {"resultCode": 401, "message": "token已过期", "data": None}
        token_data = verify_token(token)
        return {"resultCode": 200, "message": "成功", "data": token_data}
    except jwt.PyJWTError:
        return {"resultCode": 401, "message": "未登录", "data": None}