本專案使用 Kaggle 的 Fruit-360 資料集進行訓練。因容量限制，資料集與模型權重並未包含在此 GitHub 儲存庫中。請依照以下步驟設定：

請至 [Fruits-360 dataset](https://www.kaggle.com/datasets/moltean/fruits?utm_source=chatgpt.com) 下載完整資料集。

將下載的檔案解壓縮，並放置於 backend/data/fruits-360_100x100/ 目錄下。

進入 backend 目錄執行 python train.py 重新訓練模型，系統將會自動生成 .pt 權重檔並存入 backend/models/ 資料夾中。

資料來源：
[Fruits-360 dataset](https://www.kaggle.com/datasets/moltean/fruits?utm_source=chatgpt.com)

在backend中執行
uvicorn main:app --reload
可在
http://127.0.0.1:8000/docs
查看 fast API 預設的網站

在frontend中執行
npm run dev
可在
http://localhost:5173/
使用辨識網站


🍎 fruit-recognition-system/ (專案根目錄)
│
├── 📂 backend/                 # 【後端與 AI 模型區】(Python)
│   ├── 📂 data/                # 存放 Fruits-360 資料集的地方 (通常會將此加入 .gitignore)
│   ├── 📂 models/              # 存放訓練好的模型權重檔 (例如 best_model.pt)
│   ├── 📂 notebooks/           # 存放用來探索資料、畫 Loss 曲線的 Jupyter Notebook
│   ├── 📂 uploads/             # 存放使用者上傳的實體圖片 (供歷史紀錄讀取)
│   │
│   ├── model.py                # 定義 CNN 模型架構
│   ├── train.py                # 負責執行模型訓練、資料擴增的腳本
│   ├── utils.py                # 輔助函式
│   ├── main.py                 # FastAPI 伺服器主程式 (處理圖片上傳、模型預測與資料庫路由)
│   ├── database.py             # SQLite 資料庫連線設定
│   ├── models_db.py            # SQLAlchemy 資料庫資料表 (Table) 結構定義
│   ├── schemas.py              # Pydantic 資料驗證與型別定義
│   ├── crud.py                 # 資料庫的 CRUD 操作 (新增預測紀錄、查詢歷史)
│   ├── sql_app.db              # SQLite 資料庫檔案 (執行後自動生成，建議加入 .gitignore)
│   └── requirements.txt        # 紀錄後端套件依賴 (包含 torch, fastapi, sqlalchemy 等)
│
├── 📂 frontend/                # 【前端互動介面區】(React + TypeScript)
│   ├── 📂 public/              
│   ├── 📂 src/                 
│   │   ├── 📂 components/      # React 元件庫
│   │   │   ├── ImageUploader.tsx # 圖片上傳/拖曳區塊元件
│   │   │   ├── ResultCard.tsx    # 顯示預測結果與信心水準長條圖的元件
│   │   │   ├── Loader.tsx        # 等待 AI 辨識時的載入動畫元件
│   │   │   └── HistoryList.tsx   # 展示歷史辨識紀錄的卡片或清單元件
│   │   │
│   │   ├── 📂 api/             
│   │   │   └── apiClient.ts      # 封裝呼叫後端 FastAPI 的邏輯 (包含預測與取得歷史紀錄)
│   │   │
│   │   ├── 📂 types/           
│   │   │   └── index.ts          # TypeScript 型別定義 (包含預測結果與歷史紀錄介面)
│   │   │
│   │   ├── App.tsx             # 前端主畫面佈局 (包含「首頁」與「歷史紀錄」的切換機制)
│   │   └── index.css           # 全域樣式設定
│   │
│   ├── package.json            # 前端套件依賴
│   └── tsconfig.json           # TypeScript 設定檔
│
└── README.md                   # 專案說明文件 (如何啟動前後端、數據成果截圖)