# MageMirror 系统蓝图（SYSTEM BLUEPRINT）

版本：V1.0  
项目名：MageMirror（魔镜）  
创建时间：2026-03-23  

---

# 1. 项目目标

构建一个 AI 衣橱系统，实现：

- 衣物数字化管理
- AI穿搭推荐
- 天气驱动推荐
- 场景穿搭建议
- 自动生成穿搭方案
- 视觉识别衣物
- Agent自动执行任务

---

# 2. 系统总体架构

用户
 │
Web UI / Mobile
 │
FastAPI Backend
 │
Task Router
 │
AI Agent
 │
数据库
 │
文件存储

---

# 3. 核心模块

## 3.1 衣物数据库

表：

- users
- clothes
- outfits
- tags

字段结构：

(详细定义)

---

## 3.2 图像识别系统

功能：

上传图片 → 自动识别：

- 上衣
- 裤子
- 鞋
- 颜色
- 风格

使用：

- Gemini Vision API

---

## 3.3 AI推荐系统

输入：

- 天气
- 场景
- 衣物库存

输出：

- 推荐穿搭

---

## 3.4 Agent系统

功能：

自动：

- 分析天气
- 推荐穿搭
- 推送通知

---

# 4. 技术栈

Backend：

- Python 3.12
- FastAPI

Database：

- PostgreSQL

AI：

- Gemini
- OpenRouter

Storage：

- MinIO

---

# 5. 数据流设计

用户上传图片

↓

Vision识别

↓

入库

↓

AI分析

↓

生成推荐

---

# 6. 部署结构

Docker Compose：

- api
- db
- storage
- ai_agent

---

# 7. 未来扩展计划

V2：

- 自动换季推荐

V3：

- AI试衣

V4：

- AR试穿

---

# 8. 系统约束

- 所有数据必须持久化
- 所有任务必须可回溯
- 所有模块必须解耦

---

# 9. 当前版本状态

Version: V1  
Status: 开发中
