import os
import io
import glob
import uuid
import base64
import torch
import torch.nn.functional as F

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles 
from sqlalchemy.orm import Session
from PIL import Image
from torchvision import transforms
from rembg import remove

import models_db
import schemas
import crud
from database import engine, SessionLocal

# 載入我們自定義的模型架構
from model import FruitClassifier

# ==========================================
# 1. 全域變數與參數設定
# ==========================================
MODEL_DIR = './models'
DATA_DIR = './data/fruits-360_100x100/fruits-360/Training'

# 確保 uploads 資料夾存在 (必須在 FastAPI 啟動前建立)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_latest_model_path():
    list_of_files = glob.glob(os.path.join(MODEL_DIR, '*.pt'))
    if not list_of_files:
        return None
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

MODEL_PATH = get_latest_model_path()
device = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
model = None
class_names = []

# ==========================================
# 2. 初始化與資料庫設定
# ==========================================
# 建立資料庫資料表
models_db.Base.metadata.create_all(bind=engine)

# 初始化 FastAPI 應用程式
app = FastAPI(title="水果辨識系統 API", description="接收前端圖片並回傳 Top-3 辨識結果")

# 掛載靜態資料夾
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# 取得資料庫 Session 的 Dependency 函式
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# 3. CORS 跨域請求設定
# ==========================================
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 4. 伺服器啟動時的初始化邏輯
# ==========================================
@app.on_event("startup")
async def startup_event():
    global model, class_names

    if os.path.exists(DATA_DIR):
        class_names = sorted(os.listdir(DATA_DIR))
        class_names = [name for name in class_names if not name.startswith('.')]
    else:
        print(f"警告: 找不到資料夾 {DATA_DIR}，無法載入類別名稱。")
        class_names = [f"Class_{i}" for i in range(260)] 

    NUM_CLASSES = len(class_names)
    
    if MODEL_PATH is None:
        raise RuntimeError(f"在 {MODEL_DIR} 資料夾中找不到任何 .pt 模型檔案！請先執行 train.py 完成訓練。")

    print(f"伺服器啟動中... 準備載入模型，共偵測到 {NUM_CLASSES} 個類別。")
    print(f"🌟 自動鎖定最新模型: {MODEL_PATH}")

    model = FruitClassifier(num_classes=NUM_CLASSES, model_type='mobilenet_v2')
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device, weights_only=True))
    model = model.to(device)
    model.eval()
    print(f"模型已成功載入至 {device}！")

# ==========================================
# 5. 圖片前處理邏輯
# ==========================================
normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])

preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    normalize
])

# ==========================================
# 6. 定義 API 端點
# ==========================================
@app.post("/predict")
async def predict_fruit(
    file: UploadFile = File(...),
    remove_bg: bool = Form(True),
    db: Session = Depends(get_db)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="請上傳有效的圖片檔案 (JPEG/PNG)。")

    try:
        image_data = await file.read()
        
        # 產生獨一無二的檔名並將「實體圖片」存入 uploads 資料夾
        file_extension = file.filename.split(".")[-1] if "." in file.filename else "jpg"
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        with open(file_path, "wb") as f:
            f.write(image_data)

        if remove_bg:
            bg_removed_data = remove(image_data)
            rgba_image = Image.open(io.BytesIO(bg_removed_data))
            white_bg_image = Image.new("RGB", rgba_image.size, (255, 255, 255))
            white_bg_image.paste(rgba_image, mask=rgba_image.split()[3])
            input_image = white_bg_image
            
            buffered = io.BytesIO()
            rgba_image.save(buffered, format="PNG")
            processed_image_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
            processed_image_str = f"data:image/png;base64,{processed_image_b64}"
        else:
            input_image = Image.open(io.BytesIO(image_data)).convert("RGB")
            processed_image_str = None

        input_tensor = preprocess(input_image).unsqueeze(0).to(device)

        with torch.no_grad():
            outputs = model(input_tensor)
            probabilities = F.softmax(outputs, dim=1)[0]
            top3_prob, top3_catid = torch.topk(probabilities, 3)

        results = []
        for i in range(3):
            cat_id = top3_catid[i].item()
            prob = top3_prob[i].item()
            results.append({
                "rank": i + 1,
                "class_name": class_names[cat_id],
                "confidence": round(prob * 100, 2)
            })

        # 呼叫 CRUD 將紀錄寫入資料庫
        db_image_path = f"/uploads/{unique_filename}"
        prediction_record = schemas.PredictionCreate(
            image_path=db_image_path,
            predicted_class=results[0]["class_name"],
            confidence=results[0]["confidence"]
        )
        crud.create_prediction(db=db, prediction=prediction_record)

        response_data = {
            "success": True,
            "predictions": results
        }
        if processed_image_str:
            response_data["processed_image"] = processed_image_str

        return response_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"伺服器處理圖片時發生錯誤: {str(e)}")

@app.get("/history", response_model=list[schemas.PredictionResponse])
def read_history(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """
    取得過去所有的辨識紀錄 (依照時間倒序排列)。
    """
    records = crud.get_history(db, skip=skip, limit=limit)
    return records

@app.get("/")
def read_root():
    return {"message": "Fruit Recognition API is running!"}