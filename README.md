# Nutrient Collect Application

## 飲食分析資料收集工具
使用Python進行開發，搭配PyQt5介面，並串接深度攝影機，能夠記錄食物影像、深度資訊以及相對應的營養成分。
輸入餐盤區域、菜色名稱以及營養成分後，按下「儲存」，即可儲存菜色影像、深度資訊及對應的營養成分。
![](https://i.imgur.com/89mcGor.png)

#### 開發環境
- python 3.7.10

#### 執行
```shell script
python main.py
```

#### 參數設定
[config.yaml](config.yaml)為參數設定檔
- env_variables
  - app_version: 應用程式版本
  - debug: 是否顯示訊息在console上，true: 顯示；false: 不顯示
- server
  - url: 資料上傳伺服器ip
