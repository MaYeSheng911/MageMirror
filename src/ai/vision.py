import os
import json

from google import genai
from PIL import Image


# ============================
# 读取 API KEY
# ============================

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "❌ GEMINI_API_KEY 未设置"
    )

client = genai.Client(
    api_key=API_KEY
)


# ============================
# AI识别函数
# ============================

def analyze_clothes(image_path):

    try:

        print("🔥 调用 Gemini:", image_path)

        img = Image.open(
            image_path
        )

        prompt = """
你是一个服装识别专家。

请识别这张图片中的衣物，并返回 JSON：

{
"name": "",
"category": "",
"color": "",
"season": "",
"style": "",
"brand": ""
}

category 必须是：

shirt
pants
shoes
coat
jacket
sweater
shorts
dress
bag
accessory

season 必须是：

spring
summer
autumn
winter
all

style 必须是：

casual
formal
sport
business
home
outdoor

只返回 JSON，不要解释。
"""

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[
                prompt,
                img
            ]
        )

        text_result = response.text

        print("🔥 Gemini返回:", text_result)

        data = json.loads(
            text_result
        )

        return data

    except Exception as e:

        print("❌ AI识别失败:", e)

        return {

            "name": "unknown",
            "category": "unknown",
            "color": "unknown",
            "season": "unknown",
            "style": "unknown",
            "brand": "unknown"

        }
