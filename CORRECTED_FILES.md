# Corrected Full File Versions

## ✅ Complete Corrected Files

---

## 1. src/main.py (COMPLETE CORRECTED VERSION)

```python
from fastapi import FastAPI, Request
from sqlalchemy import text
from sqlalchemy.orm import Session
from config.database import engine, SessionLocal

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# 导入 router
from src.clothes import router as clothes_router
from src.storage import router as storage_router

# ================================
# 创建 FastAPI
# ================================

app = FastAPI(
    title="MageMirror API",
    version="1.0"
)


# ================================
# 注册 API
# ================================

app.include_router(clothes_router)
app.include_router(storage_router)


# ================================
# 静态资源
# ================================

app.mount(
    "/static",
    StaticFiles(
        directory="src/static"
    ),
    name="static"
)


# ================================
# 图片目录
# ================================

app.mount(
    "/image",
    StaticFiles(
        directory="uploads"
    ),
    name="images"
)


# ================================
# 模板
# ================================

templates = Jinja2Templates(
    directory="templates"
)


# ================================
# 人物主页
# ================================

@app.get("/", response_class=HTMLResponse)
def persons_page(request: Request):

    return templates.TemplateResponse(
        "persons.html",
        {
            "request": request
        }
    )


# ================================
# 获取人物列表 API
# ================================

@app.get("/persons")
def get_persons():
    """
    返回所有人物列表（JSON格式）
    """
    db: Session = SessionLocal()

    try:
        result = db.execute(
            text("""
            SELECT
                id,
                name,
                created_at
            FROM persons
            ORDER BY id ASC
            """)
        )

        persons_list = []

        for row in result:
            persons_list.append({
                "id": row.id,
                "name": row.name,
                "created_at": str(row.created_at) if row.created_at else None
            })

        return {
            "status": "success",
            "data": persons_list
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "data": []
        }

    finally:
        db.close()


# ================================
# 柜子页面
# ================================

@app.get(
    "/storage/{person_id}",
    response_class=HTMLResponse
)
def storage_page(
    request: Request,
    person_id: int
):

    return templates.TemplateResponse(
        "storage.html",
        {
            "request": request,
            "person_id": person_id
        }
    )


# ================================
# 衣服列表页面
# ================================

@app.get(
    "/clothes-page/{storage_id}",
    response_class=HTMLResponse
)
def clothes_page(
    request: Request,
    storage_id: int
):

    return templates.TemplateResponse(
        "clothes.html",
        {
            "request": request,
            "storage_id": storage_id
        }
    )


# ================================
# 衣服详情页面 ⭐
# ================================

@app.get(
    "/detail/{clothes_id}",
    response_class=HTMLResponse
)
def detail_page(
    request: Request,
    clothes_id: int
):

    return templates.TemplateResponse(
        "detail.html",
        {
            "request": request,
            "clothes_id": clothes_id
        }
    )


# ================================
# 手机上传页面
# ================================

@app.get("/mobile-upload")
def mobile_upload_page(request: Request):

    return templates.TemplateResponse(
        "mobile-upload.html",
        {
            "request": request
        }
    )


# ================================
# 上传页面（别名）
# ================================

@app.get("/upload")
def upload_page(request: Request):

    return templates.TemplateResponse(
        "mobile-upload.html",
        {
            "request": request
        }
    )


# ================================
# 数据库测试
# ================================

@app.get("/test-db")
def test_database():

    try:

        with engine.connect() as conn:

            conn.execute(
                text("SELECT 1")
            )

        return {

            "status": "success",
            "database": "connected"

        }

    except Exception as e:

        return {

            "status": "error",
            "message": str(e)

        }
```

---

## 2. src/clothes.py (Only Line 18 Changed)

```python
from fastapi import APIRouter, UploadFile, File, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from config.database import SessionLocal

from src.ai.vision import analyze_clothes
from src.ai.image_processor import process_image

from typing import List

import os
import uuid
from datetime import datetime


router = APIRouter()

UPLOAD_DIR = "uploads"  # ✅ CHANGED: was "/home/ubuntu/MageMirror/uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


# ==========================================
# 上传衣服（带AI识别）
# ==========================================

@router.post("/upload-clothes")
async def upload_clothes(
    files: List[UploadFile] = File(...),
    storage_id: int = 1
):

    db: Session = SessionLocal()

    try:

        uploaded_ids = []

        for file in files:

            file_id = str(uuid.uuid4())

            file_ext = file.filename.split(".")[-1]

            raw_name = f"{file_id}.{file_ext}"

            raw_path = os.path.join(
                UPLOAD_DIR,
                raw_name
            )

            # 保存原始图片
            with open(raw_path, "wb") as f:

                content = await file.read()

                f.write(content)

            # 图片预处理
            processed_path = process_image(
                raw_path
            )

            # =================================
            # 🔥 AI识别开始
            # =================================

            print("🔥 AI识别开始:", processed_path)

            try:

                ai_result = analyze_clothes(
                    processed_path
                )

                print("🔥 AI识别结果:", ai_result)

            except Exception as e:

                print("❌ AI识别失败:", e)

                ai_result = {}

            # fallback 防止None

            name = ai_result.get(
                "name",
                "unknown"
            )

            category = ai_result.get(
                "category",
                "unknown"
            )

            color = ai_result.get(
                "color",
                "unknown"
            )

            season = ai_result.get(
                "season",
                "unknown"
            )

            style = ai_result.get(
                "style",
                "unknown"
            )

            brand = ai_result.get(
                "brand",
                "unknown"
            )

            # =================================
            # 写入 clothes
            # =================================

            result = db.execute(
                text("""
                INSERT INTO clothes (
                    user_id,
                    storage_id,
                    name,
                    category,
                    color,
                    season,
                    style,
                    brand,
                    created_at
                )
                VALUES (
                    1,
                    :storage_id,
                    :name,
                    :category,
                    :color,
                    :season,
                    :style,
                    :brand,
                    :created_at
                )
                RETURNING id
                """),
                {

                    "storage_id": storage_id,

                    "name": name,
                    "category": category,
                    "color": color,
                    "season": season,
                    "style": style,
                    "brand": brand,

                    "created_at": datetime.now()

                }
            )

            clothes_id = result.fetchone()[0]

            # =================================
            # 写入 images
            # =================================

            db.execute(
                text("""
                INSERT INTO images (
                    clothes_id,
                    image_url,
                    is_primary,
                    created_at
                )
                VALUES (
                    :clothes_id,
                    :image_url,
                    true,
                    :created_at
                )
                """),
                {

                    "clothes_id": clothes_id,
                    "image_url": processed_path,
                    "created_at": datetime.now()

                }
            )

            uploaded_ids.append(
                clothes_id
            )

        db.commit()

        return {

            "status": "success",
            "uploaded": len(uploaded_ids),
            "ids": uploaded_ids

        }

    finally:

        db.close()


# ==========================================
# 按柜子获取衣物
# ==========================================

@router.get("/clothes-by-storage/{storage_id}")
def get_clothes_by_storage(
    storage_id: int,
    request: Request
):

    db: Session = SessionLocal()

    try:

        result = db.execute(
            text("""
            SELECT
                c.id,
                c.name,
                c.category,
                c.color,
                i.image_url
            FROM clothes c
            LEFT JOIN images i
            ON c.id = i.clothes_id
            WHERE c.storage_id = :storage_id
            ORDER BY c.created_at DESC
            """),
            {

                "storage_id": storage_id

            }
        )

        clothes_list = []

        base_url = str(
            request.base_url
        )

        for row in result:

            if row.image_url:

                image_name = os.path.basename(
                    row.image_url
                )

                image_url = (
                    base_url +
                    "image/" +
                    image_name
                )

            else:

                image_url = None

            clothes_list.append({

                "id": row.id,
                "name": row.name,
                "category": row.category,
                "color": row.color,
                "image_url": image_url

            })

        return {

            "status": "success",
            "data": clothes_list

        }

    finally:

        db.close()


# ==========================================
# 获取单件详情
# ==========================================

@router.get("/clothes/{clothes_id}")
def get_clothes_detail(
    clothes_id: int,
    request: Request
):

    db: Session = SessionLocal()

    try:

        result = db.execute(
            text("""
            SELECT
                c.id,
                c.name,
                c.category,
                c.color,
                c.season,
                c.style,
                c.brand,
                i.image_url
            FROM clothes c
            LEFT JOIN images i
            ON c.id = i.clothes_id
            WHERE c.id = :id
            """),
            {

                "id": clothes_id

            }
        )

        row = result.fetchone()

        if not row:

            return {

                "status": "error"

            }

        base_url = str(
            request.base_url
        )

        image_name = os.path.basename(
            row.image_url
        )

        image_url = (

            base_url +
            "image/" +
            image_name

        )

        return {

            "status": "success",

            "data": {

                "id": row.id,
                "name": row.name,
                "category": row.category,
                "color": row.color,
                "season": row.season,
                "style": row.style,
                "brand": row.brand,
                "image_url": image_url

            }

        }

    finally:

        db.close()
```

---

## 3. src/storage.py (NO CHANGES NEEDED)

This file was already correct and doesn't need any modifications.

```python
from fastapi import APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import text
from config.database import SessionLocal

router = APIRouter()


# ================================
# 获取某人的储物柜列表
# ================================

@router.get("/storage-units/{person_id}")
def get_storage_units(person_id: int):
    """
    获取指定用户的所有储物柜
    """
    db: Session = SessionLocal()

    try:
        result = db.execute(
            text("""
            SELECT
                id,
                name,
                location,
                created_at
            FROM storage_units
            WHERE person_id = :person_id
            ORDER BY created_at ASC
            """),
            {"person_id": person_id}
        )

        storage_list = []

        for row in result:
            storage_list.append({
                "id": row.id,
                "name": row.name,
                "location": row.location,
                "created_at": str(row.created_at) if row.created_at else None
            })

        return {
            "status": "success",
            "data": storage_list
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "data": []
        }

    finally:
        db.close()


# ================================
# 创建默认储物柜（如果不存在）
# ================================

@router.get("/storage/new/{person_id}")
def create_default_storage(person_id: int):
    """
    为指定用户创建默认储物柜（如果还没有的话）
    """
    db: Session = SessionLocal()

    try:
        # 检查是否已有储物柜
        check_result = db.execute(
            text("""
            SELECT COUNT(*) as count
            FROM storage_units
            WHERE person_id = :person_id
            """),
            {"person_id": person_id}
        )

        count = check_result.fetchone().count

        # 如果已存在,返回现有的
        if count > 0:
            existing = db.execute(
                text("""
                SELECT id, name, location
                FROM storage_units
                WHERE person_id = :person_id
                ORDER BY created_at ASC
                LIMIT 1
                """),
                {"person_id": person_id}
            ).fetchone()

            return {
                "status": "success",
                "message": "storage already exists",
                "data": {
                    "id": existing.id,
                    "name": existing.name,
                    "location": existing.location
                }
            }

        # 创建默认储物柜
        result = db.execute(
            text("""
            INSERT INTO storage_units (person_id, name, location)
            VALUES (:person_id, :name, :location)
            RETURNING id, name, location
            """),
            {
                "person_id": person_id,
                "name": "默认柜子",
                "location": "卧室"
            }
        )

        db.commit()

        new_storage = result.fetchone()

        return {
            "status": "success",
            "message": "storage created",
            "data": {
                "id": new_storage.id,
                "name": new_storage.name,
                "location": new_storage.location
            }
        }

    except Exception as e:
        db.rollback()
        return {
            "status": "error",
            "message": str(e)
        }

    finally:
        db.close()


# ================================
# 创建新储物柜（API）
# ================================

@router.post("/storage/create")
def create_storage(person_id: int, name: str = "新柜子", location: str = ""):
    """
    创建新的储物柜
    """
    db: Session = SessionLocal()

    try:
        result = db.execute(
            text("""
            INSERT INTO storage_units (person_id, name, location)
            VALUES (:person_id, :name, :location)
            RETURNING id, name, location, created_at
            """),
            {
                "person_id": person_id,
                "name": name,
                "location": location
            }
        )

        db.commit()

        new_storage = result.fetchone()

        return {
            "status": "success",
            "data": {
                "id": new_storage.id,
                "name": new_storage.name,
                "location": new_storage.location,
                "created_at": str(new_storage.created_at)
            }
        }

    except Exception as e:
        db.rollback()
        return {
            "status": "error",
            "message": str(e)
        }

    finally:
        db.close()
```

---

## Summary of Changes

### src/main.py
- ✅ Added imports: `Session`, `SessionLocal`
- ✅ Added `/persons` API endpoint (46 new lines)
- ✅ Fixed `templates` directory path (relative)
- ✅ Fixed `uploads` directory path (relative)

### src/clothes.py
- ✅ Fixed `UPLOAD_DIR` path (relative)

### src/storage.py
- ✅ No changes needed

---

## Testing

```bash
# Start server
cd /workspace/MageMirror
export PYTHONPATH=$(pwd):$PYTHONPATH
uvicorn src.main:app --reload --host 0.0.0.0 --port 8200

# Test endpoints
curl http://localhost:8200/persons
curl http://localhost:8200/test-db
curl http://localhost:8200/

# Open in browser
http://localhost:8200/
```

---

**Last Updated**: 2026-04-25  
**Status**: ✅ All Files Corrected
