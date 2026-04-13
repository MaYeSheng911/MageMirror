-- =========================================================
-- MageMirror 初始化数据表
-- version: V1.0
-- =========================================================

-- 用户表
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100),
    password_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 衣物表
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

-- 图片表
CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    clothes_id INTEGER REFERENCES clothes(id),
    image_url TEXT,
    is_primary BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 标签表
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE
);

-- 衣物标签关联表
CREATE TABLE clothes_tags (
    id SERIAL PRIMARY KEY,
    clothes_id INTEGER REFERENCES clothes(id),
    tag_id INTEGER REFERENCES tags(id)
);

-- 穿搭表
CREATE TABLE outfits (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name VARCHAR(100),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 穿搭明细
CREATE TABLE outfit_items (
    id SERIAL PRIMARY KEY,
    outfit_id INTEGER REFERENCES outfits(id),
    clothes_id INTEGER REFERENCES clothes(id)
);

-- 推荐记录
CREATE TABLE recommendations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    weather VARCHAR(50),
    occasion VARCHAR(50),
    result TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
