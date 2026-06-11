import os
import datetime
from tqdm import tqdm
import copy
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# 引用剛剛寫好的自定義模型
from model import FruitClassifier

def train_model():
    # ==========================================
    # 1. 參數設定與環境準備
    # ==========================================
    DATA_DIR = './data/fruits-360_100x100/fruits-360'  # 請根據實際資料夾結構調整路徑
    TRAIN_DIR = os.path.join(DATA_DIR, 'Training')
    VAL_DIR = os.path.join(DATA_DIR, 'Test')
    MODEL_SAVE_DIR = './models'
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    MODEL_SAVE_PATH = os.path.join(MODEL_SAVE_DIR, f'best_model_{current_time}.pt')    
    
    BATCH_SIZE = 128
    EPOCHS = 3
    LEARNING_RATE = 0.001

    # 確保模型儲存的資料夾存在
    os.makedirs(MODEL_SAVE_DIR, exist_ok=True)

    # 設定運算設備 (支援 CUDA, Apple Silicon MPS, 或 CPU)
    if torch.cuda.is_available():
        device = torch.device("cuda")
        torch.backends.cudnn.benchmark = True
    elif torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")
    print(f"目前使用的運算設備: {device}")

    # ==========================================
    # 2. 資料前處理與擴增 (Data Augmentation)
    # ==========================================
    # ImageNet 標準的正規化參數
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225])

    data_transforms = {
        'train': transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.RandomHorizontalFlip(),    # 隨機水平翻轉
            transforms.RandomRotation(15),        # 隨機旋轉 ±15 度
            transforms.ToTensor(),
            normalize
        ]),
        'val': transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            normalize
        ]),
    }

    # ==========================================
    # 3. 讀取資料集 (Datasets & DataLoaders)
    # ==========================================
    try:
        image_datasets = {
            'train': datasets.ImageFolder(TRAIN_DIR, data_transforms['train']),
            'val': datasets.ImageFolder(VAL_DIR, data_transforms['val'])
        }
    except FileNotFoundError:
        print(f"錯誤：找不到資料集！請確認 {TRAIN_DIR} 與 {VAL_DIR} 路徑正確且包含資料。")
        return
    
    class_names = image_datasets['train'].classes
    ACTUAL_NUM_CLASSES = len(class_names)
    print(f"自動偵測到的類別數量為: {ACTUAL_NUM_CLASSES}")

    dataloaders = {
        'train': DataLoader(image_datasets['train'], batch_size=BATCH_SIZE, shuffle=True, num_workers=0,pin_memory=True),
        'val': DataLoader(image_datasets['val'], batch_size=BATCH_SIZE, shuffle=False, num_workers=0,pin_memory=True)
    }

    dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}
    print(f"訓練集大小: {dataset_sizes['train']}, 驗證集大小: {dataset_sizes['val']}")
    # ==========================================
    # 4. 初始化模型、損失函數與優化器
    # ==========================================
    model = FruitClassifier(num_classes=ACTUAL_NUM_CLASSES, model_type='mobilenet_v2')
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    # ==========================================
    # 5. 訓練迴圈 (Training Loop)
    # ==========================================
    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0
    history = {'train_loss': [], 'val_loss': [], 'train_acc': [], 'val_acc': []}

    for epoch in range(EPOCHS):
        print(f'\nEpoch {epoch+1}/{EPOCHS}')
        print('-' * 20)

        # 每個 epoch 都有訓練與驗證階段
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()  # 設定為訓練模式
            else:
                model.eval()   # 設定為評估模式

            running_loss = 0.0
            running_corrects = 0

            # 迭代資料 batch
            for inputs, labels in tqdm(dataloaders[phase], desc=f"處理 {phase.capitalize()} 資料"):
                inputs = inputs.to(device)
                labels = labels.to(device)

                # 歸零梯度
                optimizer.zero_grad()

                # 前向傳播
                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    # 若在訓練階段則進行反向傳播與優化
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                # 統計損失與準確率
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            # 計算該 epoch 的平均 loss 與 accuracy
            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]

            print(f'{phase.capitalize()} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')

            # 注意：epoch_acc 是 PyTorch 的 Tensor，要用 .item() 轉成一般的 Python 數字才能畫圖
            if phase == 'train':
                history['train_loss'].append(epoch_loss)
                history['train_acc'].append(epoch_acc.item())
            else:
                history['val_loss'].append(epoch_loss)
                history['val_acc'].append(epoch_acc.item())

            # 如果是驗證階段且準確率創新高，則更新最佳權重
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())
                torch.save(best_model_wts, MODEL_SAVE_PATH)
                print(f'*** 發現新的最佳模型！已儲存至 {MODEL_SAVE_PATH} ***')

    print('\n訓練結束！')
    print(f'最佳驗證準確率: {best_acc:4f}')
    print('\n開始產生評估圖表...')
    import json
    from utils import plot_training_history, plot_confusion_matrix

    # 1. 為了怕圖表沒畫成功數據不見，先備份筆記本為 JSON 檔
    with open(os.path.join(MODEL_SAVE_DIR, 'history.json'), 'w') as f:
        json.dump(history, f)

    # 2. 畫出 Loss 與 Accuracy 的折線圖
    plot_training_history(history, save_path='./notebooks/training_metrics.png')

    # 3. 載入我們剛剛存下來的「最佳模型權重」，準備畫混淆矩陣
    model.load_state_dict(best_model_wts)
    
    # 4. 畫出混淆矩陣
    # class_names 就是我們之前用 image_datasets['train'].classes 取得的類別名稱列表
    class_names = image_datasets['train'].classes
    plot_confusion_matrix(
        model=model, 
        dataloader=dataloaders['val'], # 使用驗證集來測試
        class_names=class_names, 
        device=device, 
        save_path='./notebooks/confusion_matrix.png'
    )
    print('圖表產生完畢！')

if __name__ == '__main__':
    train_model()