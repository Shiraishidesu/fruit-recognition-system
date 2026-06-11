import React, { useState } from 'react';
import './App.css'; // 如果不需要預設樣式，這行也可刪除
import ImageUploader from './components/ImageUploader';
import HistoryList from './components/HistoryList';

// 定義頁籤的型別
type Tab = 'upload' | 'history';

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('upload');

  return (
    <div style={{ fontFamily: 'system-ui, -apple-system, sans-serif', backgroundColor: '#f4f7f6', minHeight: '100vh', paddingBottom: '40px' }}>
      
      {/* 頂部導覽列 Navbar */}
      <header style={{ 
        backgroundColor: '#fff', 
        padding: '16px 40px', 
        boxShadow: '0 2px 8px rgba(0,0,0,0.06)', 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        marginBottom: '40px'
      }}>
        <h1 style={{ margin: 0, fontSize: '22px', color: '#2c3e50', fontWeight: 'bold' }}>
          🍎 AI 智慧水果辨識系統
        </h1>
        
        {/* 切換按鈕 */}
        <nav style={{ display: 'flex', gap: '12px' }}>
          <button
            onClick={() => setActiveTab('upload')}
            style={{
              padding: '10px 20px',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontWeight: '600',
              fontSize: '15px',
              backgroundColor: activeTab === 'upload' ? '#4CAF50' : '#f0f0f0',
              color: activeTab === 'upload' ? 'white' : '#666',
              transition: 'all 0.2s ease'
            }}
          >
            📷 上傳辨識
          </button>
          <button
            onClick={() => setActiveTab('history')}
            style={{
              padding: '10px 20px',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontWeight: '600',
              fontSize: '15px',
              backgroundColor: activeTab === 'history' ? '#4CAF50' : '#f0f0f0',
              color: activeTab === 'history' ? 'white' : '#666',
              transition: 'all 0.2s ease'
            }}
          >
            🗂️ 歷史紀錄
          </button>
        </nav>
      </header>

      {/* 內容渲染區塊 */}
      <main style={{ padding: '0 20px' }}>
        {activeTab === 'upload' ? <ImageUploader /> : <HistoryList />}
      </main>

    </div>
  );
}

export default App;