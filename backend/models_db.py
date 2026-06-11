from sqlalchemy import Column, Integer, String, Float, DateTime
import datetime
from database import Base

class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String, index=True)          # 圖片在伺服器上的相對路徑
    predicted_class = Column(String, index=True)     # 第一名的辨識結果
    confidence = Column(Float)                       # 信心水準 (%)
    created_at = Column(DateTime, default=datetime.datetime.utcnow) # 建立時間 (UTC)