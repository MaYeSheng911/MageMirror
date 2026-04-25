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

        # 如果已存在，返回现有的
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
