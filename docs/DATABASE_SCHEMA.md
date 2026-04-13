# MageMirror 数据库结构设计（DATABASE SCHEMA）

版本：V1.0  
创建时间：2026-03-23  
数据库类型：PostgreSQL  

---

# 一、数据库总体说明

MageMirror 是一个：

AI衣橱管理系统

数据库核心目标：

1. 管理用户
2. 管理衣物
3. 管理穿搭组合
4. 管理标签
5. 管理图片
6. 管理推荐历史

数据库设计原则：

- 可扩展
- 可查询
- 可分析
- 可支持AI推荐

---

# 二、核心数据表结构

---

# 1. users（用户表）

用于存储系统用户信息。

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,

    username VARCHAR(50) UNIQUE NOT NULL,

    email VARCHAR(100),

    password_hash TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
字段说明：
字段
说明
id
用户ID
username
用户名
email
邮箱
password_hash
密码
created_at
创建时间

2. clothes（衣物表）
核心表之一。
存储所有衣物信息。

CREATE TABLE clothes (
    id SERIAL PRIMARY KEY,

    user_id INTEGER REFERENCES users(id),

    name VARCHAR(100),

    category VARCHAR(50),

    color VARCHAR(50),

    season VARCHAR(50),

    style VARCHAR(50),

    brand VARCHAR(100),

    purchase_date DATE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
字段说明：
字段
说明
id
衣物ID
user_id
所属用户
name
衣物名称
category
类别（上衣/裤子/鞋）
color
颜色
season
季节
style
风格
brand
品牌
purchase_date
购买时间
3. images（图片表）
用于存储衣物图片信息。
3. images（图片表）
用于存储衣物图片信息。
SQL
CREATE TABLE images (
    id SERIAL PRIMARY KEY,

    clothes_id INTEGER REFERENCES clothes(id),

    image_url TEXT,

    is_primary BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
字段说明：
字段
说明
id
图片ID
clothes_id
对应衣物
image_url
图片地址
is_primary
是否主图
4. tags（标签表）
用于分类衣物。
SQL
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,

    name VARCHAR(50) UNIQUE
);
例子：
Plain text
休闲
商务
运动
正式
夏季
冬季
5. clothes_tags（衣物标签关联表）
多对多关系表。
SQL
CREATE TABLE clothes_tags (
    id SERIAL PRIMARY KEY,

    clothes_id INTEGER REFERENCES clothes(id),

    tag_id INTEGER REFERENCES tags(id)
);
说明：
一个衣物可以有多个标签。
6. outfits（穿搭组合表）
用于存储穿搭方案。
SQL
CREATE TABLE outfits (
    id SERIAL PRIMARY KEY,

    user_id INTEGER REFERENCES users(id),

    name VARCHAR(100),

    description TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
说明：
一个 outfit 是一个完整穿搭。
7. outfit_items（穿搭明细表）
关联衣物。
SQL
CREATE TABLE outfit_items (
    id SERIAL PRIMARY KEY,

    outfit_id INTEGER REFERENCES outfits(id),

    clothes_id INTEGER REFERENCES clothes(id)
);
说明：
一个穿搭包含多个衣物。
例如：
Plain text
上衣
裤子
鞋
外套
8. recommendations（推荐记录表）
AI推荐历史。
SQL
CREATE TABLE recommendations (
    id SERIAL PRIMARY KEY,

    user_id INTEGER REFERENCES users(id),

    weather VARCHAR(50),

    occasion VARCHAR(50),

    result TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
说明：
保存：
AI给过哪些推荐。
三、类别（category）标准
衣物分类建议：
Plain text
top        上衣
pants      裤子
shoes      鞋
jacket     外套
hat        帽子
accessory  配饰
四、颜色（color）标准
Plain text
black
white
gray
blue
red
green
brown
beige
yellow
pink
五、季节（season）
Plain text
spring
summer
autumn
winter
all
六、风格（style）
Plain text
casual
formal
sport
business
street
minimal
vintage
七、数据库关系图（逻辑）
Plain text
users
   │
   ├── clothes
   │        │
   │        ├── images
   │        └── clothes_tags
   │
   ├── outfits
   │        └── outfit_items
   │
   └── recommendations
八、未来扩展（V2）
未来会增加：
Plain text
weather_cache
ai_feedback
favorite_outfits
user_preferences
九、版本记录
V1：
基础衣橱系统结构完成。
