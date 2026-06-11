import axios from 'axios';
import type { PredictResponse, HistoryRecord } from '../types'; // 引入剛剛定義的型別

// 設定後端伺服器的基礎網址
export const API_BASE_URL = 'http://localhost:8000';

/**
 * 上傳圖片至後端進行水果辨識
 * @param imageFile 使用者選擇的圖片檔案 (File 物件)
 * @returns 包含 Top-3 預測結果的 Promise
 */


// 🍎 函式新增一個 removeBg 的參數
export const predictFruit = async (imageFile: File, removeBg: boolean): Promise<PredictResponse> => {
  const formData = new FormData();
  formData.append('file', imageFile);
  
  // 🍎 將布林值轉為字串傳給後端 (FastAPI 會自動將 "true"/"false" 解析回布林值)
  formData.append('remove_bg', removeBg.toString());

  try {
    const response = await axios.post<PredictResponse>(
      `${API_BASE_URL}/predict`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error('API 呼叫發生錯誤:', error);
    throw new Error('無法連線到伺服器或圖片處理失敗，請確認後端伺服器已啟動。');
  }

  
};

export const fetchHistory = async (): Promise<HistoryRecord[]> => {
  try {
    const response = await axios.get<HistoryRecord[]>(`${API_BASE_URL}/history`);
    return response.data;
  } catch (error) {
    console.error('取得歷史紀錄發生錯誤:', error);
    throw new Error('無法取得歷史紀錄，請確認後端伺服器已啟動。');
  }
};