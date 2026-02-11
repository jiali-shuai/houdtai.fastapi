from fastapi import APIRouter, Depends, Query, HTTPException, Request
from datetime import datetime
from pydantic import BaseModel
from tortoise.expressions import Q
from typing import Optional, List
import hashlib

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from models.models import User
from core.jwt import verify_and_get_token_data


router = APIRouter()

class UserResponse(BaseModel):
    id: int
    username: str
    phone: Optional[str]
    avatar: Optional[str]
    status: int
    create_time: datetime

@router.get("/admin/user/{page}")
async def get_user_list(
    request: Request,
    page: int = 1,
    keyword: Optional[str] = None,
    phone: Optional[str] = None,
    page_size: int = 10
):
    """获取用户列表"""
    token = request.headers.get("token")
    if not token:
        return {"resultCode": 401, "message": "未授权访问", "data": None}
    
    token_data = verify_and_get_token_data(token)
    if token_data.get("resultCode") != 200:
        return token_data

    try:
        # 构建查询条件
        conditions = []
        if keyword:
            conditions.append(Q(login_name__icontains=keyword))
        if phone:
            conditions.append(Q(nick_name__icontains=phone))
        
        # 分页查询
        offset = (page - 1) * page_size
        users = await User.filter(*conditions).order_by('-create_time').limit(page_size).offset(offset)
        total = await User.filter(*conditions).count()
        
        # 格式化响应数据
        user_list = []
        for user in users:
            user_list.append({
                "id": user.user_id,
                "username": user.login_name,
                "phone": user.nick_name,
                "avatar": "http:\/\/tangzhe123-com.oss-cn-shenzhen.aliyuncs.com\/public\/681f10647924b.jpeg",
                "user_level_id": 0,
                "create_time": user.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                "update_time": user.update_time.strftime("%Y-%m-%d %H:%M:%S"),
                "last_login_time": None,
                "status": 1,
            })
        
        return {
            "resultCode": 200,
            "message": "获取成功",
            "data": {
                "list": user_list,
                "totalCount": total
            }
        }
    except Exception as e:
        return {
            "resultCode": 500,
            "message": f"获取用户列表失败: {str(e)}",
            "data": None
        }

@router.post("/admin/user")
async def create_user(request: Request, user_data: dict):
    """创建用户"""
    token = request.headers.get("token")
    if not token:
        return {"resultCode": 401, "message": "未授权访问", "data": None}
    
    token_data = verify_and_get_token_data(token)
    if token_data.get("resultCode") != 200:
        return token_data

    try:
        # 创建用户
        user = await User.create(
            login_name=user_data.get("username"),
            password_md5=hashlib.md5(user_data.get("password").encode()).hexdigest(),
            nick_name=user_data.get("phone"),
        )
        
        return {
            "resultCode": 200,
            "message": "创建成功",
            "data": {
                "id": user.user_id,
                "username": user.login_name,  # 修改为login_name
                "phone": user.nick_name,
                "create_time": user.create_time.strftime("%Y-%m-%d %H:%M:%S")
            }
        }
    except Exception as e:
        return {
            "resultCode": 500,
            "message": f"创建用户失败: {str(e)}",
            "data": None
        }

@router.post("/admin/user/{user_id}")
async def update_user(request: Request, user_id: int, user_data: dict):
    """更新用户信息"""
    token = request.headers.get("token")
    if not token:
        return {"resultCode": 401, "message": "未授权访问", "data": None}
    
    token_data = verify_and_get_token_data(token)
    if token_data.get("resultCode") != 200:
        return token_data

    try:
        # 构建更新字段字典
        update_fields = {
            "login_name": user_data.get("username")
        }
        if "phone" in user_data:
            update_fields["nick_name"] = user_data.get("phone")
        if "password" in user_data:
            update_fields["password_md5"] = hashlib.md5(user_data.get("password").encode()).hexdigest()

        # 更新用户信息
        await User.filter(user_id=user_id).update(**update_fields)
        
        # 获取更新后的用户信息
        updated_user = await User.get(user_id=user_id)
        return {
            "resultCode": 200,
            "message": "更新成功",
            "data": {
                "id": updated_user.user_id,
                "username": updated_user.login_name,
                "phone": updated_user.nick_name,
                "password": updated_user.password_md5,
                "create_time": updated_user.create_time.strftime("%Y-%m-%d %H:%M:%S")
            }
        }
    except Exception as e:
        return {
            "resultCode": 500,
            "message": f"更新用户失败: {str(e)}",
            "data": None
        }

@router.post("/admin/user/{user_id}/update_status")
async def update_user_status(request: Request, user_id: int, status_data: dict):
    """更新用户状态"""
    token = request.headers.get("token")
    if not token:
        return {"resultCode": 401, "message": "未授权访问", "data": None}
    
    token_data = verify_and_get_token_data(token)
    if token_data.get("resultCode") != 200:
        return token_data

    try:
        await User.filter(user_id=user_id).update(
            status=status_data.get("status")
        )
        return {
            "resultCode": 200,
            "message": "状态更新成功",
            "data": None
        }
    except Exception as e:
        return {
            "resultCode": 500,
            "message": f"更新用户状态失败: {str(e)}",
            "data": None
        }

@router.post("/admin/user/{user_id}/delete")
async def delete_user(request: Request, user_id: int):
    """删除用户"""
    token = request.headers.get("token")
    if not token:
        return {"resultCode": 401, "message": "未授权访问", "data": None}
    
    token_data = verify_and_get_token_data(token)
    if token_data.get("resultCode") != 200:
        return token_data

    try:
        await User.filter(user_id=user_id).delete()
        return {
            "resultCode": 200,
            "message": "删除成功",
            "data": None
        }
    except Exception as e:
        return {
            "resultCode": 500,
            "message": f"删除用户失败: {str(e)}",
            "data": None
        }