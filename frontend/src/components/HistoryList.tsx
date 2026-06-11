import React, { useState, useEffect } from 'react';
import { fetchHistory, API_BASE_URL } from '../api/apiClient';
import type { HistoryRecord } from '../types';

const HistoryList: React.FC = () => {
  const [records, setRecords] = useState<HistoryRecord[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // 元件掛載時，自動向後端拉取資料
  useEffect(() => {
    const loadHistory = async () => {
      try {
        setLoading(true);
        const data = await fetchHistory();
        setRecords(data);
      } catch (err: any) {
        setError(err.message || '發生未知錯誤');
      } finally {
        setLoading(false);
      }
    };
    loadHistory();
  }, []);

  // 狀態 1：載入中
  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px', fontSize: '18px', color: '#666' }}>
        ⏳ 正在載入歷史紀錄...
      </div>
    );
  }

  // 狀態 2：發生錯誤
  if (error) {
    return (
      <div style={{ textAlign: 'center', padding: '50px', color: 'red' }}>
        <h3>🚨 發生錯誤</h3>
        <p>{error}</p>
      </div>
    );
  }

  // 狀態 3：空白狀態 (Empty State)
  if (records.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '60px 20px', backgroundColor: '#f9f9f9', borderRadius: '10px', marginTop: '20px' }}>
        <h2 style={{ fontSize: '40px', margin: '0 0 10px 0' }}>📭</h2>
        <h3 style={{ color: '#333' }}>目前還沒有任何辨識紀錄喔！</h3>
        <p style={{ color: '#666' }}>趕快切換到「上傳辨識」頁面，測試你的第一顆水果吧。</p>
      </div>
    );
  }

  // 狀態 4：資料展示 (卡片網格佈局)
  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '20px 0' }}>
      <h2 style={{ textAlign: 'center', marginBottom: '30px', color: '#333' }}>📚 過去的辨識成果</h2>
      
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', // 自動響應式網格
        gap: '20px'
      }}>
        {records.map((record) => (
          <div key={record.id} style={{
            border: '1px solid #eaeaea',
            borderRadius: '12px',
            overflow: 'hidden',
            backgroundColor: '#fff',
            boxShadow: '0 4px 12px rgba(0,0,0,0.05)',
            transition: 'transform 0.2s',
            cursor: 'default'
          }}>
            {/* 圖片縮圖區塊 */}
            <div style={{ height: '180px', backgroundColor: '#f0f0f0', display: 'flex', justifyContent: 'center', alignItems: 'center', overflow: 'hidden' }}>
              <img 
                src={`${API_BASE_URL}${record.image_path}`} 
                alt={record.predicted_class} 
                style={{ width: '100%', height: '100%', objectFit: 'cover' }} 
                // 圖片讀取失敗時的備用處理
                onError={(e) => { (e.target as HTMLImageElement).style.display = 'none'; }}
              />
            </div>
            
            {/* 數據資訊區塊 */}
            <div style={{ padding: '16px' }}>
              <h3 style={{ margin: '0 0 12px 0', fontSize: '18px', color: '#222' }}>{record.predicted_class}</h3>
              
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                <span style={{ fontSize: '14px', color: '#777' }}>信心水準</span>
                <span style={{ fontWeight: 'bold', color: '#4CAF50' }}>{record.confidence}%</span>
              </div>
              
              {/* 長條圖視覺化 */}
              <div style={{ width: '100%', backgroundColor: '#eee', height: '6px', borderRadius: '3px', marginBottom: '15px' }}>
                <div style={{ width: `${record.confidence}%`, backgroundColor: '#4CAF50', height: '100%', borderRadius: '3px' }}></div>
              </div>
              
              {/* 時間戳記 */}
              <div style={{ fontSize: '12px', color: '#aaa', textAlign: 'right', borderTop: '1px solid #eee', paddingTop: '10px' }}>
                {new Date(record.created_at).toLocaleString('zh-TW')}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default HistoryList;