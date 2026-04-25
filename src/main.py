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
