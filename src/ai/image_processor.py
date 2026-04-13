from rembg import remove
from PIL import Image
import io
import os


# ===== 去背景 + 压缩 =====

def process_image(input_path):

    output_path = input_path.replace(
        ".jpg",
        ".png"
    ).replace(
        ".jpeg",
        ".png"
    )

    # ===== 读取图片 =====

    with open(input_path, "rb") as f:
        input_bytes = f.read()

    # ===== 去背景 =====

    output_bytes = remove(input_bytes)

    # ===== 转为 PIL =====

    image = Image.open(
        io.BytesIO(output_bytes)
    )

    # ===== 统一尺寸 =====

    image.thumbnail(
        (512, 512)
    )

    # ===== 压缩保存 =====

    image.save(
        output_path,
        format="PNG",
        optimize=True
    )

    return output_path
