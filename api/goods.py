from fastapi import APIRouter, Depends, Query, HTTPException, Request
from datetime import datetime
from pydantic import BaseModel
from tortoise.expressions import Q
from typing import Optional,List

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from models.models import Goods
from core.jwt import verify_and_get_token_data

router = APIRouter()

class GoodsResponse(BaseModel):
    id: int  # 改为前端使用的字段名
    title: str  # 改为goodsName的映射
    cover: str  # 改为goodsCoverImg的映射
    min_price: float  # 改为sellingPrice的映射
    ISBN: Optional[str]
    author: Optional[str]
    press: Optional[str]
    stock: Optional[int]
    create_time: datetime # 新增销量字段，默认0

@router.get("/admin/goods/{page}")
async def get_goods_list(
    request: Request,
    page: int = 1,
    title: Optional[str] = Query(None),
    ISBN: Optional[str] = Query(None),
    tab: Optional[str] = Query("all"),  # 新增tab参数
    page_size: int = 10
):
    """获取商品列表"""
    token = request.headers.get("token")
    if not token:
        return {"resultCode": 401, "message": "未授权访问", "data": None}
    
    token_data = verify_and_get_token_data(token)
    if token_data.get("resultCode") != 200:
        return token_data

    try:
        # 构建查询条件
        conditions = []
        if title:
            conditions.append(Q(goodsName__icontains=title))
        if ISBN:
            conditions.append(Q(ISBN__icontains=ISBN))
        elif tab == "delete":
            conditions.append(Q(is_delete=1))
        
        # 分页查询
        offset = (page - 1) * page_size
        goods = await Goods.filter(*conditions).limit(page_size).offset(offset)
        total = await Goods.filter(*conditions).count()
        
        # 格式化响应数据
        # 在get_goods_list路由中修改返回数据格式
        items = [{
            "id": g.goodsId,
            "title": g.goodsName,
            "cover": g.goodsCoverImg or "",
            "min_price": float(g.sellingPrice),
            "ISBN": g.ISBN,
            "author": g.author,
            "press": g.press,
            "stock": g.stock,
            "create_time": g.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            # 以下是固定返回的字段
            "desc": "哈哈哈哈啊11商品描述",
            "content": "<!DOCTYPE html>\n<html>\n<head>\n<\/head>\n<body>\n<p>&nbsp;<img style=\"width: 100%;\" src=\"http:\/\/tangzhe123-com.oss-cn-shenzhen.aliyuncs.com\/public\/61c773e91e874.png\" \/> &nbsp;<img style=\"width: 100%;\" src=\"http:\/\/tangzhe123-com.oss-cn-shenzhen.aliyuncs.com\/public\/61c773d716296.png\" \/>&nbsp;123456<\/p>\n<table style=\"border-collapse: collapse; width: 100%;\" border=\"1\">\n<tbody>\n<tr>\n<td style=\"width: 24.4165%;\">&nbsp;<\/td>\n<td style=\"width: 24.4165%;\">&nbsp;<\/td>\n<td style=\"width: 24.4165%;\">&nbsp;<\/td>\n<td style=\"width: 24.4165%;\">&nbsp;<\/td>\n<\/tr>\n<tr>\n<td style=\"width: 24.4165%;\">&nbsp;<\/td>\n<td style=\"width: 24.4165%;\">&nbsp;<\/td>\n<td style=\"width: 24.4165%;\">&nbsp;<\/td>\n<td style=\"width: 24.4165%;\">&nbsp;<\/td>\n<\/tr>\n<tr>\n<td style=\"width: 24.4165%;\">&nbsp;<\/td>\n<td style=\"width: 24.4165%;\">&nbsp;<\/td>\n<td style=\"width: 24.4165%;\">&nbsp;<\/td>\n<td style=\"width: 24.4165%;\">&nbsp;<\/td>\n<\/tr>\n<tr>\n<td style=\"width: 24.4165%;\">&nbsp;<\/td>\n<td style=\"width: 24.4165%;\">&nbsp;<\/td>\n<td style=\"width: 24.4165%;\">&nbsp;<\/td>\n<td style=\"width: 24.4165%;\">&nbsp;<\/td>\n<\/tr>\n<\/tbody>\n<\/table>\n",
            "discount": 0,
            "update_time": "2025-02-11 12:54:31",
            "delete_time": None,
            "goods_banner": [
                {
                    "id": 2440,
                    "goods_id": 49,
                    "url": "http:\/\/tangzhe123-com.oss-cn-shenzhen.aliyuncs.com\/public\/680902c2bcd6d.jpg",
                    "create_time": "2025-05-15 14:58:24",
                    "update_time": "2025-05-15 14:58:24"
                },
            ],
        } for g in goods]
        
        return {
            "resultCode": 200,
            "message": "获取成功",
            "data": {
                "list": items,
                "totalCount": total
            }
        }
    except Exception as e:
        return {
            "resultCode": 500,
            "message": f"获取商品列表失败: {str(e)}",
            "data": None
        }
        
@router.post("/admin/goods/delete_all")
async def delete_all_goods(request: Request):
    """批量删除商品"""
    token = request.headers.get("token")
    if not token:
        return {"resultCode": 401, "message": "未授权访问", "data": None}
    
    token_data = verify_and_get_token_data(token)
    if token_data.get("resultCode") != 200:
        return token_data

    try:
        # 从请求体中获取商品ID列表
        data = await request.json()
        goods_ids = data.get("ids", [])
        
        if not goods_ids:
            return {
                "resultCode": 400,
                "message": "请提供要删除的商品ID列表", 
                "data": None
            }

        await Goods.filter(goodsId__in=goods_ids).delete()
        return {
            "resultCode": 200,
            "message": "批量删除成功",
            "data": None
        }
    except Exception as e:
        return {
            "resultCode": 500,
            "message": f"批量删除失败: {str(e)}",
            "data": None
        }



@router.post("/admin/goods")
async def create_goods(request: Request, goods_data: dict):
    """创建商品"""
    token = request.headers.get("token")
    if not token:
        return {"resultCode": 401, "message": "未授权访问", "data": None}
    
    token_data = verify_and_get_token_data(token)
    if token_data.get("resultCode") != 200:
        return token_data

    try:
        # 创建商品基础信息
        goods = await Goods.create(
            goodsName=goods_data.get("title"),
            sellingPrice=goods_data.get("min_price"),
            goodsCoverImg=goods_data.get("cover"),
            goods_detail_content=goods_data.get("desc"),
            ISBN=goods_data.get("ISBN"),
            author=goods_data.get("author"),
            press=goods_data.get("press"),
            stock=goods_data.get("stock", 100),
        )
        
        # 返回创建成功的响应
        return {
            "resultCode": 200,
            "message": "创建成功",
            "data": {
                "id": goods.goodsId,
                "title": goods.goodsName,
                "cover": goods.goodsCoverImg or "",
                "min_price": float(goods.sellingPrice),
                "desc": goods.goods_detail_content,
                "ISBN": goods.ISBN,
                "author": goods.author,
                "press": goods.press,
                "stock": goods.stock,
                "create_time": goods.create_time.strftime("%Y-%m-%d %H:%M:%S")
            }
        }
    except Exception as e:
        return {
            "resultCode": 500,
            "message": f"创建商品失败: {str(e)}",
            "data": None
        }

@router.post("/admin/goods/{goods_id}")
async def update_goods(request: Request, goods_id: int, goods_data: dict):
    """更新商品"""
    token = request.headers.get("token")
    if not token:
        return {"resultCode": 401, "message": "未授权访问", "data": None}
    
    token_data = verify_and_get_token_data(token)
    if token_data.get("resultCode") != 200:
        return token_data

    try:
        # 获取现有商品信息
        goods = await Goods.get(goodsId=goods_id)
        
        # 更新商品信息，使用get方法提供默认值
        await Goods.filter(goodsId=goods_id).update(
            goodsName=goods_data.get("title", goods.goodsName),
            sellingPrice=goods_data.get("min_price", goods.sellingPrice),
            goodsCoverImg=goods_data.get("cover", goods.goodsCoverImg),
            goods_detail_content=goods_data.get("desc", goods.goods_detail_content),
            ISBN=goods_data.get("ISBN", goods.ISBN),
            author=goods_data.get("author", goods.author),
            press=goods_data.get("press", goods.press),
            stock=goods_data.get("stock", goods.stock),
        )
        
        # 获取更新后的商品信息
        updated_goods = await Goods.get(goodsId=goods_id)
        return {
            "resultCode": 200,
            "message": "更新成功",
            "data": {
                "id": updated_goods.goodsId,
                "title": updated_goods.goodsName,
                "cover": updated_goods.goodsCoverImg or "",
                "min_price": float(updated_goods.sellingPrice),
                "desc": updated_goods.goods_detail_content,
                "ISBN": updated_goods.ISBN,
                "author": updated_goods.author,
                "press": updated_goods.press,
                "stock": updated_goods.stock,
                "create_time": updated_goods.create_time.strftime("%Y-%m-%d %H:%M:%S")
            }
        }
    except Exception as e:
        return {
            "resultCode": 500,
            "message": f"更新商品失败: {str(e)}",
            "data": None
        }






