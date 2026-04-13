import os
from sqlalchemy.orm import Session
from sqlalchemy import text

from config.database import SessionLocal
from ai.vision import analyze_clothes


UPLOAD_DIR = "/home/ubuntu/MageMirror/uploads"


def fix_unknown_clothes():

    db: Session = SessionLocal()

    try:

        print("🚀 开始重新识别 unknown 衣物")

        result = db.execute(
            text("""
            SELECT
                c.id,
                i.image_url
            FROM clothes c
            LEFT JOIN images i
            ON c.id = i.clothes_id
            WHERE c.category = 'unknown'
            """)
        )

        rows = result.fetchall()

        print("📦 发现数量:", len(rows))

        for row in rows:

            clothes_id = row.id

            if not row.image_url:
                continue

            image_name = os.path.basename(
                row.image_url
            )

            image_path = os.path.join(
                UPLOAD_DIR,
                image_name
            )

            if not os.path.exists(
                image_path
            ):
                print("⚠️ 文件不存在:", image_path)
                continue

            print("🔍 识别:", image_path)

            try:

                ai_result = analyze_clothes(
                    image_path
                )

                print("✅ 结果:", ai_result)

            except Exception as e:

                print("❌ 失败:", e)

                continue

            db.execute(
                text("""
                UPDATE clothes
                SET
                    name = :name,
                    category = :category,
                    color = :color,
                    season = :season,
                    style = :style,
                    brand = :brand
                WHERE id = :id
                """),
                {

                    "id": clothes_id,

                    "name": ai_result.get(
                        "name",
                        "unknown"
                    ),

                    "category": ai_result.get(
                        "category",
                        "unknown"
                    ),

                    "color": ai_result.get(
                        "color",
                        "unknown"
                    ),

                    "season": ai_result.get(
                        "season",
                        "unknown"
                    ),

                    "style": ai_result.get(
                        "style",
                        "unknown"
                    ),

                    "brand": ai_result.get(
                        "brand",
                        "unknown"
                    )

                }
            )

            db.commit()

        print("🎉 处理完成")

    finally:

        db.close()


if __name__ == "__main__":

    fix_unknown_clothes()
