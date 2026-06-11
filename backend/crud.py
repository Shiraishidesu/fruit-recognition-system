from sqlalchemy.orm import Session
import models_db
import schemas

def create_prediction(db: Session, prediction: schemas.PredictionCreate):
    # 將 Pydantic schema 轉換為 SQLAlchemy ORM 模型
    db_prediction = models_db.PredictionHistory(**prediction.model_dump())
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction) # 刷新以取得自動產生的 id 與 created_at
    return db_prediction

def get_history(db: Session, skip: int = 0, limit: int = 50):
    # 查詢歷史紀錄，並透過 order_by 將最新的紀錄排在最前面
    return db.query(models_db.PredictionHistory)\
             .order_by(models_db.PredictionHistory.created_at.desc())\
             .offset(skip).limit(limit).all()