from pydantic import BaseModel, ConfigDict
from datetime import datetime

# 寫入資料庫時需要的欄位 (不需要 id 與 created_at，因為資料庫會自動產生)
class PredictionCreate(BaseModel):
    image_path: str
    predicted_class: str
    confidence: float

# 從資料庫讀取、回傳給前端時的完整欄位
class PredictionResponse(PredictionCreate):
    id: int
    created_at: datetime
    
    # 允許 Pydantic 直接讀取 SQLAlchemy 的 ORM 模型
    model_config = ConfigDict(from_attributes=True)