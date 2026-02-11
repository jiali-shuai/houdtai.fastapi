from fastapi import APIRouter, Depends, Query, HTTPException, Request
from datetime import datetime
from pydantic import BaseModel
from tortoise.expressions import Q
from typing import Optional, List

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from models.models import Order, OrderItem, User,Address
from core.jwt import verify_and_get_token_data

router = APIRouter()

class OrderResponse(BaseModel):
    id: int
    no: str
    user_id: int
    total_price: float
    payment_method: str
    paid_time: Optional[datetime]
    create_time: datetime
    status: str
    refund_status: Optional[str]
    ship_data: Optional[dict]
    address: Optional[dict]
    order_items: List[dict]

@router.get("/admin/order/{page}")
async def get_order_list(
    request: Request,
    page: int=1,
    no: Optional[str] = None,
    phone: Optional[str] = None,
    tab: Optional[str] = None,
    page_size: Optional[int] = None
):
    """获取订单列表"""
    token = request.headers.get("token")
    if not token:
        return {"resultCode": 401, "message": "未授权访问", "data": None}
    
    token_data = verify_and_get_token_data(token)
    if token_data.get("resultCode") != 200:
        return token_data

    try:
        # 根据tab参数设置不同的订单状态条件
        status_map = {
            "all": None,  # 全部订单
            "noship": 1,  # 已付款未发货(对应order_status=1)
            "finish": 3   # 已完成(对应order_status=3)
        }
        
        # 构建查询条件
        conditions = []
        if no:
            conditions.append(Q(order_no__icontains=no))
        if phone:
            conditions.append(Q(user__addresses__user_phone__icontains=phone))
        if tab and tab in status_map and status_map[tab] is not None:
            conditions.append(Q(order_status=status_map[tab]))
        
        # 分页处理
        page_size = page_size or 10
        offset = (page - 1) * page_size
        
        # 查询订单数据，预加载用户地址
        # 查询订单数据，按创建时间倒序排列
        orders = await Order.filter(*conditions).prefetch_related(
            "user", "user__addresses", "items", "items__goods"
        ).order_by("-create_time").limit(page_size).offset(offset)  # 添加.order_by("-create_time")
        
        # 格式化响应数据
        items = []
        for order in orders:
            # 获取用户默认地址
            default_address = await order.user.addresses.filter(default_flag=1).first()
            if not default_address:
                default_address = await order.user.addresses.first()
            
            # 构建订单项列表
            order_items = []
            for item in order.items:
                order_items.append({
                    "id": item.order_item_id,
                    "order_id": order.order_id,
                    "goods_id": item.goods_id,
                    "num": item.goods_count,
                    "price": str(item.selling_price),
                    "goods_item": {
                        "id": item.goods_id,
                        "title": item.goods_name,
                        "cover": item.goods_cover_img,
                    },
                })
            
            items.append({
                "id": order.order_id,
                "no": order.order_no,
                "user_id": order.user_id,
                "address": {
                    "id": default_address.address_id if default_address else None,
                    "user_id": order.user_id,
                    "province": default_address.province_name if default_address else None,
                    "city": default_address.city_name if default_address else None,
                    "district": default_address.region_name if default_address else None,
                    "address": default_address.detail_address if default_address else None,
                    "zip": 2123000,  # 固定值，与示例一致
                    "name": default_address.user_name if default_address else order.user.login_name,
                    "phone": default_address.user_phone if default_address else order.user.nick_name,
                    "last_used_time": 1639064591,  # 固定值，与示例一致
                    "create_time": default_address.create_time.strftime("%Y-%m-%d %H:%M:%S") if default_address else None,
                    "update_time": default_address.update_time.strftime("%Y-%m-%d %H:%M:%S") if default_address else None
                },
                "total_price": str(order.total_price),
                "remark": "",  # 空字符串，与示例一致
                "paid_time": int(order.pay_time.timestamp()) if order.pay_time else None,
                "ship_status": "pending" if order.order_status < 2 else "delivered",
                "payment_method": "alipay" if order.pay_type == 1 else "wechat",
                "payment_no": "2019122622001446221403706833",  # 固定值，与示例一致
                "refund_status": "pending",  # 固定值，与示例一致
                "refund_no": None,  # None，与示例一致
                "closed": 0,  # 固定值，与示例一致
                "ship_status": "pending" if order.order_status < 2 else "delivered",
                "ship_data": None,  # None，与示例一致
                "extra": None,  # None，与示例一致
                "create_time": order.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                "update_time": order.update_time.strftime("%Y-%m-%d %H:%M:%S"),
                "reviewed": 0,  # 固定值，与示例一致
                "coupon_user_id": 0,  # 固定值，与示例一致
                "order_items": order_items,
                "user": {
                    "id": order.user.user_id,
                    "nickname": order.user.nick_name or "昵称",
                    "username": order.user.login_name,
                    "avatar": "https://tangzhe123-com.oss-cn-shenzhen.aliyuncs.com/Appstatic/qsbk/demo/userpic/6.jpg"
                }
            })
        
        # Calculate total count of orders matching the conditions
        total = await Order.filter(*conditions).count()
        
        return {
            "resultCode": 200,
            "message": "获取成功", 
            "data": {
                "list": items,
                "tota_Count": total  # Use the calculated total count
            }
        }
    except Exception as e:
        return {
            "resultCode": 500,
            "message": f"获取订单列表失败: {str(e)}",
            "data": None
        }


@router.post("/admin/order/{id}/ship")
async def ship_order(
    request: Request,
    id: int,
    data: dict
):
    """订单发货接口"""
    # 验证token
    token = request.headers.get("token")
    if not token:
        return {"resultCode": 401, "message": "未授权访问", "data": None}
    
    token_data = verify_and_get_token_data(token)
    if token_data.get("resultCode") != 200:
        return token_data

    try:
        # 更新订单状态为3(已发货)
        await Order.filter(order_id=id).update(
            order_status=3,
            ship_time=datetime.now()
        )
        
        return {
            "resultCode": 200,
            "message": "发货成功",
            "data": None
        }
    except Exception as e:
        return {
            "resultCode": 500,
            "message": f"发货失败: {str(e)}",
            "data": None
        }

