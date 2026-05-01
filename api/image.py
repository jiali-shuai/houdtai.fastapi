from fastapi import APIRouter,Request, UploadFile, File
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

sys.path.append(str(Path(__file__).parent.parent))
from models.models import Image
from core.jwt import verify_and_get_token_data

router = APIRouter()


@router.get("/admin/image_class/{id}/image/{page}")
async def get_image_list(
    request: Request,
    image_class_id: int=1,
    page: int = 1,
    page_size: int = 10
):
    """获取指定分类下的图片列表"""
    # 获取请求头中的token
    token = request.headers.get("token")
    # 如果没有token，返回未授权访问
    if not token:
        return {"resultCode": 401, "message": "未授权访问", "data": None}
    
    # 验证token并获取token数据
    token_data = verify_and_get_token_data(token)
    # 如果token验证失败，返回错误信息
    if token_data.get("resultCode") != 200:
        return token_data

    try:
        # 分页处理
        offset = (page - 1) * page_size
        
        # 查询图片数据
        images = await Image.filter(
            image_class_id=image_class_id
        ).order_by("-create_time").limit(page_size).offset(offset)
        
        # 格式化响应数据，完全匹配Image模型字段
        items = [{
            "image_id": img.image_id,
            "name": img.name,
            "url": img.url,
            "image_class_id": img.image_class_id,
            "create_time": img.create_time.strftime("%Y-%m-%d %H:%M:%S")
        } for img in images]
        
        # 计算总数
        total = await Image.filter(image_class_id=image_class_id).count()
        
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
            "message": f"获取图片列表失败: {str(e)}",
            "data": None
        }


@router.get("/admin/image_class/{page}")
async def get_image_class_list(
    request: Request,
    page: int,
    page_size: int = 10
):
    """获取图片分类列表"""
    token = request.headers.get("token")
    if not token:
        return {"resultCode": 401, "message": "未授权访问", "data": None}
    
    token_data = verify_and_get_token_data(token)
    if token_data.get("resultCode") != 200:
        return token_data

    try:
        # 获取所有不同的图片分类ID
        distinct_classes = await Image.all().distinct().values("image_class_id")
        class_ids = [item["image_class_id"] for item in distinct_classes]
        
        # 分页处理
        offset = (page - 1) * page_size
        paginated_ids = class_ids[offset:offset+page_size]
        
        # 获取每个分类的信息

   
        
        return {
            "resultCode": 200,
            "message": "获取成功",
            "data": {
                "list": [{
                    "id": 1,
                    "name": "图片",
                    "order": 1,
                    "images_count": 1,
                    
                }],
                "totalCount": 1
            }
        }
    except Exception as e:
        return {
            "resultCode": 500,
            "message": f"获取分类信息失败: {str(e)}",
            "data": None
        }





@router.post("/admin/image/upload")
async def upload_image(
    request: Request,
    img: UploadFile = File(None),  # 参数名改为img
    image_class_id: int = 1
):
    """上传PNG图片"""
    token = request.headers.get("token")
    if not token:
        return {"resultCode": 401, "message": "未授权访问", "data": None}
    
    token_data = verify_and_get_token_data(token)
    if token_data.get("resultCode") != 200:
        return token_data

    try:
        if img is None or img.filename == "":
            return {
                "resultCode": 400,
                "message": "请提供图片文件",
                "data": None
            }

        os.makedirs("static", exist_ok=True)
        
        # 生成保存路径
        file_path = f"static/{img.filename}"
    
        # 保存文件
        with open(file_path, "wb") as buffer:
            buffer.write(await img.read())
        
        # 生成完整URL
        image_url = f"{os.getenv('SERVER_URL')}/{file_path}"
        
        # 保存到数据库
        image = await Image.create(
            name=img.filename,
            url=image_url,  # 存储完整URL
            image_class_id=image_class_id
        )
        
        return {
            "resultCode": 200,
            "message": "上传成功", 
            "data": {
                "filename": img.filename,
                "id": image.image_id,
                "url": image_url  # 返回完整URL
            }
        }
    except Exception as e:
        return {
            "resultCode": 500,
            "message": f"上传失败: {str(e)}",
            "data": None
        }
    finally:
        if img is not None:  # 关闭img文件
            img.file.close()

@router.post("/admin/image/{id}")
async def update_image(
    request: Request,
    id: int,  # 参数名改为id以匹配前端
    data: dict
):
    """更新图片信息"""
    token = request.headers.get("token")
    if not token:
        return {"resultCode": 401, "message": "未授权访问", "data": None}
    
    token_data = verify_and_get_token_data(token)
    if token_data.get("resultCode") != 200:
        return token_data

    try:
        # 更新图片名称
        await Image.filter(image_id=id).update(
            name=data.get("name")
        )
        
        return {
            "resultCode": 200,
            "message": "更新成功",
            "data": None
        }
    except Exception as e:
        return {
            "resultCode": 500,
            "message": f"更新图片失败: {str(e)}",
            "data": None
        }



@router.post("/admin/image/delete_all")
async def delete_images(
    request: Request,
    data: dict
):
    """批量删除图片"""
    token = request.headers.get("token")
    if not token:
        return {"resultCode": 401, "message": "未授权访问", "data": None}
    
    token_data = verify_and_get_token_data(token)
    if token_data.get("resultCode") != 200:
        return token_data

    try:
        ids = data.get("ids", [])  # 参数名改为ids以匹配前端
        if not ids:
            return {
                "resultCode": 400,
                "message": "请提供要删除的图片ID列表",
                "data": None
            }

        await Image.filter(image_id__in=ids).delete()
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







