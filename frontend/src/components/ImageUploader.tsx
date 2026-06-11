import React, { useState } from 'react';
import { predictFruit } from '../api/apiClient';
import type { PredictResponse } from '../types';

const ImageUploader: React.FC = () => {
  // 定義元件的狀態 (State)
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [result, setResult] = useState<PredictResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [useRembg, setUseRembg] = useState<boolean>(true); 

  // 處理使用者選擇圖片的事件
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      // 產生一個本地端的預覽網址
      setPreviewUrl(URL.createObjectURL(file));
      // 清空先前的結果與錯誤訊息
      setResult(null);
      setError(null);
    }
  };

  // 處理點擊「開始辨識」按鈕的事件
  const handleUpload = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setError(null);

    try {
      // 呼叫我們剛剛寫好的 apiClient 函式
      const data = await predictFruit(selectedFile, useRembg);
      setResult(data);
    } catch (err: any) {
      setError(err.message || '發生未知錯誤');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '500px', margin: '0 auto', textAlign: 'center', padding: '20px' }}>
      <h2>🍎 水果辨識系統</h2>
      
      {/* 圖片上傳區塊 */}
      <div style={{ marginBottom: '20px' }}>
        <input 
          type="file" 
          accept="image/*" 
          onChange={handleFileChange} 
          style={{ marginBottom: '10px' }}
        />
      </div>

      {/* 圖片預覽區塊 */}
      {previewUrl && (
        <div style={{ marginBottom: '20px' }}>
          <img 
            src={previewUrl} 
            alt="預覽圖片" 
            style={{ maxWidth: '100%', maxHeight: '300px', borderRadius: '8px', objectFit: 'cover' }} 
          />
        </div>
      )}

      {/* 去背功能開關 */}
      <div style={{ marginBottom: '15px' }}>
        <label style={{ cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
          <input
            type="checkbox"
            checked={useRembg}
            onChange={(e) => setUseRembg(e.target.checked)}
            style={{ width: '18px', height: '18px', cursor: 'pointer' }}
          />
          <span style={{ fontSize: '16px', color: '#7d6c6c' }}>啟用 AI 自動去背</span>
        </label>
      </div>

      {/* 辨識按鈕 */}
      <button 
        onClick={handleUpload} 
        disabled={!selectedFile || loading}
        style={{
          padding: '10px 20px',
          fontSize: '16px',
          backgroundColor: loading || !selectedFile ? '#ccc' : '#4CAF50',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: loading || !selectedFile ? 'not-allowed' : 'pointer'
        }}
      >
        {loading ? 'AI 辨識中...' : '開始辨識'}
      </button>

      {/* 錯誤訊息顯示 */}
      {error && (
        <div style={{ color: 'red', marginTop: '20px' }}>
          <p>{error}</p>
        </div>
      )}

      {/* 辨識結果與去背圖片顯示 */}
      {result && result.success && (
        <div style={{ marginTop: '30px', textAlign: 'left', backgroundColor: '#f9f9f9', padding: '20px', borderRadius: '8px' }}>
          
          <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap', alignItems: 'flex-start' }}>
            
            {/* 左側：AI 擷取的主體圖片 */}
            {result.processed_image && (
              <div style={{ flex: '1', minWidth: '200px', textAlign: 'center' }}>
                <h4 style={{ marginTop: 0 }}>✂️ AI 擷取主體</h4>
                {/* 加上一個棋盤格背景，讓透明去背的效果更明顯 */}
                <div style={{
                  backgroundImage: 'repeating-linear-gradient(45deg, #ccc 25%, transparent 25%, transparent 75%, #ccc 75%, #ccc), repeating-linear-gradient(45deg, #ccc 25%, #fff 25%, #fff 75%, #ccc 75%, #ccc)',
                  backgroundPosition: '0 0, 10px 10px',
                  backgroundSize: '20px 20px',
                  borderRadius: '8px',
                  padding: '10px'
                }}>
                  <img 
                    src={result.processed_image} 
                    alt="去背後的水果" 
                    style={{ maxWidth: '100%', maxHeight: '200px', objectFit: 'contain' }} 
                  />
                </div>
              </div>
            )}

            {/* 右側：Top-3 辨識結果 */}
            <div style={{ flex: '2', minWidth: '250px' }}>
              <h3 style={{ marginTop: 0 }}>✨ 辨識結果 (Top 3)</h3>
              <ul style={{ listStyleType: 'none', padding: 0 }}>
                {result.predictions.map((pred) => (
                  <li key={pred.rank} style={{ marginBottom: '10px', fontSize: '18px' }}>
                    <strong>第 {pred.rank} 名：</strong> {pred.class_name} 
                    <span style={{ float: 'right', color: '#555' }}>
                      機率：{pred.confidence}%
                    </span>
                    <div style={{ width: '100%', backgroundColor: '#ddd', height: '10px', borderRadius: '5px', marginTop: '5px' }}>
                      <div style={{ width: `${pred.confidence}%`, backgroundColor: '#4CAF50', height: '100%', borderRadius: '5px' }}></div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
            
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageUploader;