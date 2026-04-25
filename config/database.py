from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# =====================================
# 数据库连接地址
# =====================================

DATABASE_URL = "postgresql://magemirror_user:MageMirror2026@localhost:5432/mage_mirror"

# =====================================
# 创建数据库引擎
# =====================================

engine = create_engine(
    DATABASE_URL,
    echo=True
)

# =====================================
# 创建 Session
# =====================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# =====================================
# 基础模型
# =====================================

Base = declarative_base()

# =====================================
# 获取数据库 Session
# =====================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
