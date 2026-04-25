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

UPLOAD_DIR = "uploads"

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
