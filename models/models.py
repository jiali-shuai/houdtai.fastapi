from tortoise.models import Model
from tortoise import fields

class Image(Model):
    image_id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    url = fields.CharField(max_length=255)
    image_class_id = fields.IntField()
    create_time = fields.DatetimeField(auto_now_add=True)
    class Meta:
        table = "image"

class Goods(Model):
    goodsId = fields.IntField(pk=True)
    goodsName = fields.CharField(max_length=100)
    sellingPrice = fields.DecimalField(max_digits=10, decimal_places=2)
    goodsCoverImg = fields.CharField(max_length=255, null=True)
    goods_detail_content = fields.CharField(max_length=500, null=True)
    goods_detail_images = fields.JSONField(default=list)  # 修改为JSONField存储图片URL数组
    ISBN = fields.CharField(max_length=50, null=True)  # 新增ISBN字段
    author = fields.CharField(max_length=100, null=True)  # 新增作者字段
    press = fields.CharField(max_length=100, null=True)  # 新增出版社字段
    stock = fields.IntField(default=0)  # 新增库存字段，默认值为0
    create_time = fields.DatetimeField(auto_now_add=True)
    update_time = fields.DatetimeField(auto_now=True)
    
    class Meta:
        table = "goods"


class User(Model):
    user_id = fields.IntField(pk=True)
    login_name = fields.CharField(max_length=50, unique=True)
    password_md5 = fields.CharField(max_length=32)
    nick_name = fields.CharField(max_length=50, null=True)
    create_time = fields.DatetimeField(auto_now_add=True)
    update_time = fields.DatetimeField(auto_now=True)
    
    class Meta:
        table = "user"

class Cart(Model):
    # 购物车项ID，主键
    car_id = fields.IntField(pk=True) 
    # 用户外键，使用标准的模型引用方式
    user = fields.ForeignKeyField('models.User', related_name='carts', source_field='user_id')
    # 商品外键
    goods = fields.ForeignKeyField('models.Goods', related_name='carts', source_field='goods_id')
    # 商品数量，默认为1
    goods_count = fields.IntField(default=1)
    # 创建时间，自动添加当前时间
    create_time = fields.DatetimeField(auto_now_add=True)
    # 更新时间，自动更新当前时间
    update_time = fields.DatetimeField(auto_now=True)
    
    class Meta:
        table = "cart"

class Address(Model):
    # 地址ID，主键
    address_id = fields.IntField(pk=True)
    # 关联用户
    user = fields.ForeignKeyField('models.User', related_name='addresses', source_field='user_id')
    # 收货人姓名
    user_name = fields.CharField(max_length=50)
    # 收货人电话
    user_phone = fields.CharField(max_length=20)
    # 省份
    province_name = fields.CharField(max_length=255, null=True)
    # 城市
    city_name = fields.CharField(max_length=255, null=True)
    # 区域
    region_name = fields.CharField(max_length=255, null=True)
    # 详细地址
    detail_address = fields.CharField(max_length=255)
    # 是否默认地址(0-非默认 1-默认)
    default_flag = fields.IntField(default=0)
    # 创建时间
    create_time = fields.DatetimeField(auto_now_add=True)
    # 更新时间
    update_time = fields.DatetimeField(auto_now=True)
    
    class Meta:
        table = "address"

class Order(Model):
    # 订单ID，主键
    order_id = fields.IntField(pk=True)
    # 订单号
    order_no = fields.CharField(max_length=50, unique=True)
    # 关联用户
    user = fields.ForeignKeyField('models.User', related_name='orders', source_field='user_id')
    # 总价
    total_price = fields.DecimalField(max_digits=10, decimal_places=2)
    # 订单状态(0-待付款 1-已付款 2-已发货 3-已完成 4-已取消)
    order_status = fields.IntField(default=0)
    # 支付状态(0-未支付 1-已支付)
    pay_status = fields.IntField(default=0)
    # 支付类型(1-支付宝 2-微信 3-银行卡)
    pay_type = fields.IntField(null=True)
    # 支付时间
    pay_time = fields.DatetimeField(null=True)
    # 创建时间
    create_time = fields.DatetimeField(auto_now_add=True)
    # 更新时间
    update_time = fields.DatetimeField(auto_now=True)
    ship_time = fields.DatetimeField(null=True)  # 新增发货时间字段
    
    class Meta:
        table = "order"

class OrderItem(Model):
    # 订单项ID，主键
    order_item_id = fields.IntField(pk=True)
    # 关联订单
    order = fields.ForeignKeyField('models.Order', related_name='items', source_field='order_id')
    # 关联商品
    goods = fields.ForeignKeyField('models.Goods', related_name='order_items', source_field='goods_id')
    # 商品数量
    goods_count = fields.IntField()
    # 商品名称
    goods_name = fields.CharField(max_length=100)
    # 商品封面图
    goods_cover_img = fields.CharField(max_length=255)
    # 销售价
    selling_price = fields.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        table = "order_item"



class Admin(Model):
    user_id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=32)
    create_time = fields.DatetimeField(auto_now_add=True)
    update_time = fields.DatetimeField(auto_now=True)
    
    class Meta:
        table = "admin"

