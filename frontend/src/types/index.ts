// 定義單一水果的預測結果
export interface PredictionResult {
  rank: number;
  class_name: string;
  confidence: number;
}

// 定義後端 API 完整的 JSON 回傳格式
export interface PredictResponse {
  success: boolean;
  predictions: PredictionResult[];
  processed_image?: string;
}

// 新增：歷史紀錄的型別定義
export interface HistoryRecord {
  id: number;
  image_path: string;       // 例如: "/uploads/xxx.jpg"
  predicted_class: string;
  confidence: number;
  created_at: string;       // ISO 格式的時間字串
}