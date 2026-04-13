from fastapi import FastAPI, Request
from sqlalchemy import text
from config.database import engine

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# 导入 router
from src.clothes import router as clothes_router

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
        directory="/home/ubuntu/MageMirror/uploads"
    ),
    name="images"
)


# ================================
# 模板
# ================================

templates = Jinja2Templates(
    directory="/home/ubuntu/MageMirror/templates"
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
