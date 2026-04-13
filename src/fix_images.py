from sqlalchemy.orm import Session
from sqlalchemy import text
from config.database import SessionLocal

import os

UPLOAD_DIR = "/home/ubuntu/MageMirror/uploads"

db: Session = SessionLocal()

try:

    print("开始修复图片路径...")

    query_sql = """
    SELECT id, image_url
    FROM images
    """

    result = db.execute(text(query_sql))

    rows = result.fetchall()

    count = 0

    for row in rows:

        old_path = row.image_url

        if not old_path:
            continue

        image_name = os.path.basename(old_path)

        # 强制 JPG → PNG
        new_name = image_name.replace(".jpg", ".png")

        new_path = os.path.join(
            UPLOAD_DIR,
            new_name
        )

        # 检查 PNG 是否存在
        if os.path.exists(new_path):

            update_sql = """
            UPDATE images
            SET image_url = :new_path
            WHERE id = :id
            """

            db.execute(
                text(update_sql),
                {
                    "new_path": new_path,
                    "id": row.id
                }
            )

            count += 1

    db.commit()

    print(f"修复完成，共更新 {count} 条记录")

except Exception as e:

    db.rollback()

    print("错误:", e)

finally:

    db.close()
