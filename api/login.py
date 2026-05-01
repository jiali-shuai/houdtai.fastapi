from fastapi import APIRouter, Request
from tortoise.exceptions import DoesNotExist

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from core.jwt import create_access_token, verify_and_get_token_data
from models.models import Admin

router = APIRouter()



@router.post("/admin/login")
async def login(request: Request):
    # 获取前端发送的JSON数据
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    
    # 验证字段非空
    if not username or not password:
        return {
            "resultCode": 400,
            "message": "用户名和密码不能为空",
            "data": None
        }
    
    try:
        user = await Admin.get(username=username)
        if user.password != password:
            return {
                "resultCode": 400,
                "message": "用户名或密码错误",
                "data": None
            }
            
        # 修改为使用 user_id 而不是 id
        token = create_access_token({"sub": str(user.user_id)})
        
        # 返回成功响应
        return {
            "resultCode": 200,
            "message": "登录成功",
            "data": {
                "token": token
            }
        }
        
    except DoesNotExist:
        return {
            "resultCode": 400,
            "message": "用户名或密码错误",
            "data": None
        }


@router.post("/admin/getinfo")
async def getinfo(request: Request):
    # 从请求头获取token
    token = request.headers.get("token")
    if not token:
        return {
            "msg": "error",
            "data": None
        }
    
    # 验证token
    token_data = verify_and_get_token_data(token)
    if token_data.get("resultCode") != 200:
        return token_data
    
    try:
        # 返回完全匹配前端要求的数据结构
        return {
            "msg": "ok",
            "data": {
                "id": 3,
                "username": "admin",
                "avatar": "http:\/\/tangzhe123-com.oss-cn-shenzhen.aliyuncs.com\/public\/62af03d1b2aeb.jpg",
                "super": 1,
                "role": {
                    "id": 2,
                    "name": "超级管理员"
                },
                "menus": [
                    {
                        "id": 5,
                        "rule_id": 0,
                        "status": 1,
                        "create_time": "2019-08-11 13:36:09",
                        "update_time": "2019-08-11 13:36:09",
                        "name": "后台面板",
                        "desc": "index",
                        "frontpath": None,
                        "condition": None,
                        "menu": 1,
                        "order": 1,
                        "icon": "help",
                        "method": "GET",
                        "child": [
                            {
                                "id": 10,
                                "rule_id": 5,
                                "status": 1,
                                "create_time": "2019-08-11 13:37:02",
                                "update_time": "2019-08-11 13:37:02",
                                "name": "主控台",
                                "desc": "index",
                                "frontpath": "\/",
                                "condition": None,
                                "menu": 1,
                                "order": 20,
                                "icon": "home-filled",
                                "method": "GET",
                                "child": []
                            }
                        ]
                    },
                    {
                        "id": 6,
                        "rule_id": 0,
                        "status": 1,
                        "create_time": "2019-08-11 13:36:36",
                        "update_time": "2021-12-21 19:37:11",
                        "name": "商品管理",
                        "desc": "shop_goods_list",
                        "frontpath": "/goods",  # 修改为前端路由的基础路径
                        "condition": None,
                        "menu": 1,
                        "order": 2,
                        "icon": "shopping-bag",
                        "method": "GET",
                        "child": [
                            {
                                "id": 13,
                                "rule_id": 6,
                                "status": 1,
                                "create_time": "2019-12-28 13:42:13",
                                "update_time": "2021-12-21 20:21:42",
                                "name": "商品列表",  # 修正名称
                                "desc": "shop_goods_list",
                                "frontpath": "/goods/list",  # 确保路径正确
                                "condition": "",
                                "menu": 1,
                                "order": 20,
                                "icon": "shopping-cart-full",
                                "method": "GET",
                                "child": []
                            },
                            {
                                "id": 14,
                                "rule_id": 6,
                                "status": 1,
                                "create_time": "2019-12-28 13:44:00",
                                "update_time": "2021-12-21 20:22:00",
                                "name": "分类管理",
                                "desc": "shop_category_list",
                                "frontpath": "/category/list",
                                "condition": "",
                                "menu": 1,
                                "order": 20,
                                "icon": "menu",
                                "method": "GET",
                                "child": []
                            },
                    
                        ]
                    }, 
                    {
                    "id": 173,
                    "rule_id": 0,
                    "status": 1,
                    "create_time": "2021-12-21 19:38:21",
                    "update_time": "2021-12-21 19:38:21",
                    "name": "用户管理",
                    "desc": "",
                    "frontpath": "",
                    "condition": "",
                    "menu": 1,
                    "order": 3,
                    "icon": "user",
                    "method": "GET",
                    "child": [
                        {
                            "id": 21,
                            "rule_id": 173,
                            "status": 1,
                            "create_time": "2019-12-28 13:46:45",
                            "update_time": "2021-12-21 20:22:35",
                            "name": "用户管理",
                            "desc": "user_user-list_list",
                            "frontpath": "/user/list",
                            "condition": "",
                            "menu": 1,
                            "order": 20,
                            "icon": "user-filled",
                            "method": "GET",
                            "child": []
                        },
                            ]
                    },
                    {
                    "id": 7,
                    "rule_id": 0,
                    "status": 1,
                    "create_time": "2019-08-11 13:36:40",
                    "update_time": "2021-12-21 19:37:18",
                    "name": "订单管理",
                    "desc": "order_order_list",
                    "frontpath":None,
                    "condition":None,
                    "menu": 1,
                    "order": 4,
                    "icon": "message-box",
                    "method": "GET",
                    "child": [
                        {
                            "id": 18,
                            "rule_id": 7,
                            "status": 1,
                            "create_time": "2019-12-28 13:45:42",
                            "update_time": "2021-12-21 20:23:02",
                            "name": "订单管理",
                            "desc": "order_order_list",
                            "frontpath": "/order/list",
                            "condition": "",
                            "menu": 1,
                            "order": 1,
                            "icon": "reading",
                            "method": "GET",
                            "child": []
                        },
                    ]
                    },
                    {
                    "id": 9,
                    "rule_id": 0,
                    "status": 1,
                    "create_time": "2019-08-11 13:36:50",
                    "update_time": "2021-12-21 19:10:15",
                    "name": "系统设置",
                    "desc": "set_base",
                    "frontpath": None,
                    "condition": None,
                    "menu": 1,
                    "order": 6,
                    "icon": "setting",
                    "method": "GET",
                    "child": [
                        {
                            "id": 23,
                            "rule_id": 9,
                            "status": 1,
                            "create_time": "2019-12-28 13:47:15",
                            "update_time": "2021-12-21 20:23:12",
                            "name": "基础设置",
                            "desc": "set_base",
                            "frontpath": "/setting/base",
                            "condition": "",
                            "menu": 1,
                            "order": 19,
                            "icon": "baseball",
                            "method": "GET",
                            "child": []
                        },
                        ]
                    },
                    {
                        "id": 26,
                        "rule_id": 9,
                        "status": 1,
                        "create_time": "2019-12-28 13:47:57",
                        "update_time": "2021-12-21 20:23:22",
                        "name": "交易设置",
                        "desc": "set_payment",
                        "frontpath": "/setting/buy",
                        "condition": "",
                        "menu": 1,
                        "order": 20,
                        "icon": "credit-card",
                        "method": "GET",
                        "child": []
                    }, 
                    {
                    "id": 1,
                    "rule_id": 0,
                    "status": 1,
                    "create_time": "2021-12-21 19:10:34",
                    "update_time": "2021-12-21 19:10:47",
                    "name": "其他模块",
                    "desc": "",
                    "frontpath": "",
                    "condition": "",
                    "menu": 1,
                    "order": 1,
                    "icon": "mostly-cloudy",
                    "method": "GET",
                    "child": [
                        {
                            "id": 1,
                            "rule_id": 1,
                            "status": 1,
                            "create_time": "2019-12-28 13:38:32",
                            "update_time": "2021-12-21 20:23:43",
                            "name": "图库管理",
                            "desc": "image",
                            "frontpath": "/image/list",
                            "condition": None,
                            "menu": 1,
                            "order": 1,
                            "icon": "picture-filled",
                            "method": "GET",
                            "child": []
                        },
                        {
                            "id": 149,
                            "rule_id": 172,
                            "status": 1,
                            "create_time": "2021-06-11 23:21:24",
                            "update_time": "2021-12-21 20:23:33",
                            "name": "公告管理",
                            "desc": "set_notice",
                            "frontpath": "/notice/list",
                            "condition": "",
                            "menu": 1,
                            "order": 50,
                            "icon": "notification",
                            "method": "GET",
                            "child": []
                        }
                    ]
                    }
                ],  # 这里确保menus数组正确闭合
                "ruleNames": [
            "createRule,POST",
            "updateRule,POST",
            "deleteRule,POST",
            "getRuleList,GET",
            "updateRuleStatus,POST",
            "createRole,POST",
            "updateRole,POST",
            "deleteRole,POST",
            "getRoleList,GET",
            "updateRoleStatus,POST",
            "getGoodsList,GET",
            "getCurrentImageList,GET",
            "getImageClassList,GET",
            "createImageClass,POST",
            "updateImageClass,POST",
            "deleteImageClass,POST",
            "uploadImage,POST",
            "deleteImage,POST",
            "updateImage,POST",
            "getCategoryList,GET",
            "createCategory,POST",
            "sortCategory,POST",
            "updateCategory,POST",
            "updateCategoryStatus,POST",
            "deleteCategory,DELETE",
            "getSkusList,GET",
            "createSkus,POST",
            "deleteSkus,POST",
            "updateSkus,POST",
            "updateSkusStatus,POST",
            "getOrderList,GET",
            "deleteOrder,POST",
            "shipOrder,POST",
            "refundOrder,POST",
            "exportOrder,POST",
            "getCommentList,GET",
            "reviewComment,POST",
            "updateCommentStatus,POST",
            "getUserList,GET",
            "createUser,POST",
            "updateUser,POST",
            "updateUserStatus,POST",
            "deleteUser,POST",
            "getUserLevelList,GET",
            "createUserLevel,POST",
            "updateUserLevel,POST",
            "updateUserLevelStatus,POST",
            "deleteUserLevel,POST",
            "deleteManager,POST",
            "getManagerList,GET",
            "createManager,POST",
            "updateManager,POST",
            "updateManagerStatus,POST",
            "getSysSetting,GET",
            "sysconfigUpload,POST",
            "setSysSetting,POST",
            "getSysSetting,GET",
            "setSysSetting,GET",
            "readGoods,GET",
            "updateGoodsSkus,POST",
            "setGoodsBanner,POST",
            "restoreGoods,POST",
            "destroyGoods,POST",
            "deleteGoods,POST",
            "updateGoodsStatus,POST",
            "createGoods,POST",
            "updateGoods,POST",
            "checkGoods,POST",
            "createGoodsSkusCard,POST",
            "sortGoodsSkusCard,POST",
            "updateGoodsSkusCard,POST",
            "deleteGoodsSkusCard,POST",
            "createGoodsSkusCardValue,POST",
            "updateGoodsSkusCardValue,POST",
            "deleteGoodsSkusCardValue,POST",
            "getNoticeList,GET",
            "createNotice,POST",
            "updateNotice,POST",
            "deleteNotice,POST",
            "getCouponList,GET",
            "createCoupon,POST",
            "updateCoupon,POST",
            "updateCouponStatus,POST",
            "getCategoryGoods,GET",
            "connectCategoryGoods,POST",
            "deleteCategoryGoods,POST",
            "getStatistics1,GET",
            "getStatistics2,GET",
            "getStatistics3,GET",
            "setRoleRules,POST",
            "deleteCoupon,POST",
            "getShipInfo,GET",
            "getExpressCompanyList,GET",
            "getAgentStatistics,GET",
            "getAgentList,GET",
            "getUserBillList,GET",
            "getDistributionSetting,GET",
            "setDistributionSetting,POST"
                            # 其他权限规则...
                        ]
                    }
                }
        
    except DoesNotExist:

        return {
            "resultCode": 400,
            "message": "管理员不存在",
            "data": None
        }
    


