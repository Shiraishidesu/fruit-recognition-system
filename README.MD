本專案為gemini 協助完成，且使用 Kaggle 的 Fruit-360 資料集進行訓練。因容量限制，資料集與模型權重並未包含在此 GitHub 儲存庫中。請依照以下步驟設定：

請至 [Fruits-360 dataset](https://www.kaggle.com/datasets/moltean/fruits?utm_source=chatgpt.com) 下載完整資料集。

將下載的檔案解壓縮，並放置於 backend/data 目錄下。

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


# 🍎 水果辨識系統 (Fruit Recognition System)

這是一個基於卷積神經網路 (CNN) 開發的水果圖片辨識系統。本專案採前後端分離架構設計，不僅實作了從資料集處理到模型訓練的完整 AI 流程，還結合了 Web 互動介面與資料庫儲存功能，提供直覺的即時影像辨識與歷史紀錄查詢服務。

## ✨ 專案特色 (Features)

* **🧠 深度學習影像辨識**：使用 PyTorch 建構 CNN 模型（支援遷移學習），基於 Kaggle Fruits-360 資料集訓練。
* **🌐 現代化 Web 介面**：使用 React 與 TypeScript 開發，提供流暢的圖片上傳、預覽與資料視覺化體驗（Top-3 預測機率長條圖）。
* **⚡ 高效能後端 API**：使用 FastAPI 構建，具備非同步處理能力，快速回應前端的預測請求。
* **💾 歷史紀錄資料庫**：內建 SQLite 與 SQLAlchemy ORM，自動儲存使用者的辨識紀錄與實體圖片檔案，方便後續查詢與管理。

---

## 🛠️ 技術棧 (Tech Stack)

* **前端 (Frontend)**: React, TypeScript, Axios, CSS/Tailwind
* **後端 (Backend)**: Python, FastAPI, Uvicorn, SQLAlchemy
* **人工智慧 (AI/DL)**: PyTorch, Torchvision, OpenCV, Scikit-learn
* **資料庫 (Database)**: SQLite

---

## 📂 專案架構 (Project Structure)

```text
fruit-recognition-system/
│
├── backend/                    # 【後端與 AI 模型區】(Python)
│   ├── data/                   # 存放 Fruits-360 資料集的地方 (請加入 .gitignore)
│   ├── models/                 # 存放訓練好的模型權重檔 (例如 best_model.pt)
│   ├── notebooks/              # 存放用來探索資料、畫 Loss/Accuracy 曲線的 Jupyter Notebook
│   ├── uploads/                # 存放使用者上傳的實體圖片 (供歷史紀錄讀取)
│   │
│   ├── model.py                # 定義 CNN 模型架構
│   ├── train.py                # 負責執行模型訓練、資料擴增的腳本
│   ├── utils.py                # 輔助函式 (成效評估圖表產生等)
│   ├── main.py                 # FastAPI 伺服器主程式 (處理圖片上傳、預測與路由)
│   ├── database.py             # SQLite 資料庫連線設定
│   ├── models_db.py            # SQLAlchemy 資料庫資料表結構定義
│   ├── schemas.py              # Pydantic 資料驗證與型別定義
│   ├── crud.py                 # 資料庫的 CRUD 操作邏輯
│   ├── sql_app.db              # SQLite 資料庫檔案 (執行後自動生成)
│   └── requirements.txt        # 紀錄後端套件依賴清單
│
├── frontend/                   # 【前端互動介面區】(React + TypeScript)
│   ├── public/                 # 靜態資源
│   ├── src/                    
│   │   ├── components/         # React 獨立元件庫
│   │   │   ├── ImageUploader.tsx # 圖片上傳區塊
│   │   │   ├── ResultCard.tsx    # 預測結果展示卡片
│   │   │   ├── Loader.tsx        # 載入中動畫
│   │   │   └── HistoryList.tsx   # 歷史辨識紀錄列表
│   │   │
│   │   ├── api/                
│   │   │   └── apiClient.ts      # 封裝呼叫後端 FastAPI 的請求邏輯
│   │   │
│   │   ├── types/              
│   │   │   └── index.ts          # TypeScript 全域型別定義
│   │   │
│   │   ├── App.tsx             # 前端主畫面佈局與狀態管理
│   │   └── index.css           # 全域樣式設定
│   │
│   ├── package.json            # 前端套件依賴與腳本
│   └── tsconfig.json           # TypeScript 設定檔
│
└── README.md                   # 專案說明文件