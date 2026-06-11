import os
import json
import torch
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

def plot_training_history(history_path_or_dict, save_path='./notebooks/training_metrics.png'):
    """
    繪製並儲存 Loss 與 Accuracy 的折線圖
    
    Args:
        history_path_or_dict (str 或 dict): JSON 檔案路徑或直接傳入歷史紀錄字典
        save_path (str): 圖表儲存路徑
    """
    # 如果傳入的是路徑，則讀取 JSON 檔案
    if isinstance(history_path_or_dict, str):
        with open(history_path_or_dict, 'r') as f:
            history = json.load(f)
    else:
        history = history_path_or_dict

    epochs = range(1, len(history['train_loss']) + 1)

    # 建立 1 列 2 欄的畫布
    plt.figure(figsize=(14, 5))

    # 1. 繪製 Loss 曲線
    plt.subplot(1, 2, 1)
    plt.plot(epochs, history['train_loss'], 'b-', label='Training Loss')
    plt.plot(epochs, history['val_loss'], 'r-', label='Validation Loss')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)

    # 2. 繪製 Accuracy 曲線
    plt.subplot(1, 2, 2)
    plt.plot(epochs, history['train_acc'], 'b-', label='Training Accuracy')
    plt.plot(epochs, history['val_acc'], 'r-', label='Validation Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True)

    # 確保排版不重疊並儲存
    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"📈 訓練指標折線圖已成功儲存至: {save_path}")


def plot_confusion_matrix(model, dataloader, class_names, device, save_path='./notebooks/confusion_matrix.png'):
    """
    使用測試集計算預測結果，並繪製混淆矩陣熱力圖
    
    Args:
        model (nn.Module): 訓練好的 PyTorch 模型
        dataloader (DataLoader): 測試集 (Validation/Test) 的 DataLoader
        class_names (list): 類別名稱列表 (用於座標軸標籤)
        device (torch.device): 運算設備 (cuda/mps/cpu)
        save_path (str): 熱力圖儲存路徑
    """
    model.eval()
    all_preds = []
    all_labels = []

    print("正在使用測試集生成混淆矩陣數據 (推論中)...")
    with torch.no_grad():
        for inputs, labels in dataloader:
            inputs = inputs.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            
            # 將數據搬回 CPU 並轉為 numpy 陣列紀錄
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    # 計算混淆矩陣
    cm = confusion_matrix(all_labels, all_preds)
    
    # 💡 提示：Fruits-360 有 131 類，矩陣非常巨大，畫布必須夠大才不會擠在一起
    plt.figure(figsize=(24, 20))
    
    # 使用 seaborn 繪製熱力圖
    # fmt='d' 表示用整數顯示, cmap 選擇藍色調
    sns.heatmap(cm, annot=False, cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    
    plt.title('Confusion Matrix', fontsize=20)
    plt.ylabel('Actual Label', fontsize=14)
    plt.xlabel('Predicted Label', fontsize=14)
    
    # 旋轉標籤避免重疊
    plt.xticks(rotation=90, fontsize=8)
    plt.yticks(rotation=0, fontsize=8)
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"📊 混淆矩陣熱力圖已成功儲存至: {save_path}")