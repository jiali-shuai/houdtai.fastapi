# FastAPI 电商后端

一个基于 FastAPI 构建的电商后台后端服务，提供完整的电商功能接口。

## 功能特性

- 用户管理（注册、登录、个人信息、状态管理）
- 商品管理（商品列表、详情、搜索、添加、编辑、删除）
- 购物车功能
- 收货地址管理
- 订单管理（下单、发货、查询）
- 图片管理（上传、分类、列表）
- 管理员登录认证

## 技术栈

- **Web 框架**：FastAPI
- **数据库 ORM**：Tortoise-ORM
- **数据库**：MySQL
- **身份认证**：JWT
- **异步处理**：async/await

## 快速开始

1. 安装依赖：
    ```bash
    pip install -r requirements.txt
    ```

2. 配置环境变量：
    ```bash
    # 复制 .env.example 为 .env
    # 编辑 .env 文件，填入你的配置
    ```

3. 运行项目：
    ```bash
    python main.py
    ```

4. 访问接口文档：
    - Swagger UI: http://127.0.0.1:1080/docs
    - ReDoc: http://127.0.0.1:1080/redoc