import torch
import torch.nn as nn
from torchvision import models

class FruitClassifier(nn.Module):
    def __init__(self, num_classes: int = 131, model_type: str = 'mobilenet_v2'):
        """
        水果辨識系統模型 (使用遷移學習)
        
        Args:
            num_classes (int): 總分類類別數量，預設為 Fruits-360 的 131 類。
            model_type (str): 使用的預訓練模型架構，支援 'mobilenet_v2' 或 'resnet18'。
        """
        super(FruitClassifier, self).__init__()
        self.model_type = model_type.lower()
        
        if self.model_type == 'mobilenet_v2':
            # 載入預訓練的 MobileNetV2 模型 (使用預設的最佳權重)
            weights = models.MobileNet_V2_Weights.DEFAULT
            self.model = models.mobilenet_v2(weights=weights)
            
            # 取得原始分類器中，最後一層線性層的輸入特徵維度
            in_features = self.model.classifier[1].in_features
            
            # 替換最後一層全連接層，將輸出數量改為我們的目標類別數
            self.model.classifier[1] = nn.Linear(in_features, num_classes)
            
        elif self.model_type == 'resnet18':
            # 載入預訓練的 ResNet18 模型
            weights = models.ResNet18_Weights.DEFAULT
            self.model = models.resnet18(weights=weights)
            
            # 取得原始全連接層的輸入特徵維度
            in_features = self.model.fc.in_features
            
            # 替換最後一層全連接層
            self.model.fc = nn.Linear(in_features, num_classes)
            
        else:
            raise ValueError("目前僅支援 'mobilenet_v2' 或 'resnet18' 作為 model_type 參數")

    def forward(self, x):
        """
        定義模型的前向傳播 (Forward Pass)
        """
        return self.model(x)

# ---------------------------------------------------------
# 以下為簡單的測試代碼，僅在直接執行此檔案時運行，
# 當其他檔案 (如 train.py 或 main.py) import 此模組時不會觸發。
# ---------------------------------------------------------
if __name__ == "__main__":
    # 測試參數
    TEST_NUM_CLASSES = 131
    TEST_MODEL_TYPE = 'mobilenet_v2'
    
    # 實例化模型
    print(f"正在初始化 {TEST_MODEL_TYPE} 模型，目標類別數: {TEST_NUM_CLASSES}...")
    model = FruitClassifier(num_classes=TEST_NUM_CLASSES, model_type=TEST_MODEL_TYPE)
    
    # 建立一筆模擬輸入資料 (Batch Size: 1, Channels: 3, Height: 224, Width: 224)
    # 這是 PyTorch 影像分類模型標準的輸入維度
    dummy_input = torch.randn(1, 3, 224, 224)
    
    # 進行前向傳播測試
    output = model(dummy_input)
    
    print("模型測試成功！")
    print(f"輸入 Tensor 維度: {dummy_input.shape}")
    print(f"輸出 Tensor 維度: {output.shape} (預期應為 [1, {TEST_NUM_CLASSES}])")