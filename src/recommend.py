from fastapi import APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import text
from config.database import SessionLocal

from google import genai

import os
import json

router = APIRouter()

# ========= 初始化 Gemini =========

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL_ID = "gemini-2.5-flash"


# ========= 推荐接口 =========

@router.post("/recommend-outfit")
def recommend_outfit():

    db: Session = SessionLocal()

    try:

        # ========= 1. 读取衣柜 =========

        query_sql = """
        SELECT
            category,
            color,
            season,
            style
        FROM clothes
        WHERE category != 'unknown'
        """

        result = db.execute(text(query_sql))

        clothes_list = []

        for row in result:

            clothes_list.append({

                "category": row.category,
                "color": row.color,
                "season": row.season,
                "style": row.style

            })

        if not clothes_list:

            return {

                "status": "error",

                "message": "no valid clothes found"

            }

        # ========= 2. 构造 Prompt =========

        prompt = f"""
You are a fashion assistant.

Wardrobe:

{json.dumps(clothes_list, indent=2)}

Task:

Recommend ONE outfit.

Return JSON only.

Format:

{{
  "top": "",
  "bottom": "",
  "reason": ""
}}
"""

        # ========= 3. 调用 Gemini =========

        response = client.models.generate_content(

            model=MODEL_ID,

            contents=prompt

        )

        ai_text = response.text

        print("\n===== RAW AI TEXT =====")
        print(ai_text)
        print("=======================\n")

        # ========= 4. JSON 清洗 =========

        clean_text = ai_text.strip()

        # 去掉 ```json
        if clean_text.startswith("```json"):
            clean_text = clean_text.replace("```json", "", 1)

        # 去掉 ```
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]

        clean_text = clean_text.strip()

        print("\n===== CLEAN JSON =====")
        print(clean_text)
        print("======================\n")

        # ========= 5. 解析 JSON =========

        parsed = json.loads(clean_text)

        return {

            "status": "success",

            "outfit": parsed

        }

    except Exception as e:

        print("\n===== ERROR =====")
        print(str(e))
        print("=================\n")

        return {

            "status": "error",

            "message": str(e)

        }

    finally:

        db.close()
