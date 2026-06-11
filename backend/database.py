from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite 資料庫檔案會建立在 backend 目錄下，命名為 sql_app.db
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# 建立資料庫引擎 (check_same_thread=False 是 FastAPI 搭配 SQLite 時的必要設定)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 建立 Session 類別，用來在 CRUD 中與資料庫對話
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 宣告 Base，稍後我們的 ORM 模型都會繼承它
Base = declarative_base()