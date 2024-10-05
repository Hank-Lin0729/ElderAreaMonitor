# 智慧光訊長者監控系統

本專案是為長者提供區域監控與警告通知功能，透過 Arduino 傳輸長者所在區域及編號，並使用 Flask 搭配 SQLite 資料庫進行後端管理。前端則提供簡單的用戶介面以顯示和管理監控資訊。

## 功能概述

- **註冊/登入**：用戶可以註冊帳號或登入系統來管理監控功能。
- **區域監控**：Arduino 會將長者的編號及所在區域資訊上傳至伺服器，伺服器會根據不同的編號及區域存入資料庫。
- **警告通知**：當長者誤闖危險區域，或者長時間未移動等情況時，系統會顯示警告訊息，並透過 Line 通知相關照護者。
- **模擬功能**：系統支援模擬午餐時間及長時間未移動的情境，用於測試長者的行為及相應的通知功能。

## 文件結構

- **app.py**：主 Flask 應用程式，負責後端邏輯，包括資料存儲與資料獲取的 API。
- **templates/**：包含前端 HTML 檔案，如 `index.html`、`sign.html`、`signup.html` 等，用戶可透過這些頁面進行操作。
- **static/**：包含 `main.css` 和 `main.js` 等前端資源，用於定義頁面的樣式及互動邏輯。

## 安裝與設定

1. **安裝相依套件**：

   ```
  pip install flask sqlite3 werkzeug
   ```


2. **初始化資料庫**：

執行應用程式後，資料庫會自動初始化，並建立所需的資料表。

3. **啟動應用程式**：

```
python app.py
```

應用程式將會在 `http://localhost:10000` 啟動。

## API 介面

- **GET `/`**：主頁面，用戶可在此登入。
- **GET `/register`**：註冊頁面，供新用戶註冊。
- **POST `/login`**：用戶登入，成功後會重定向至主頁。
- **GET `/data/place<place_id>`**：根據不同的區域編號（如 104、105、106）獲取長者的位置數據。

## 使用說明

1. 註冊帳號並登入。
2. 使用管理面板來檢視長者的狀態。
3. 點擊區域卡片可以查看詳細的移動紀錄。
4. 模擬功能可用於測試午餐時間或長時間未移動的情境。

## 前端互動邏輯

`main.js` 定義了頁面上多項互動，包括：
- **時間顯示**：顯示當前時間，並每秒更新一次。
- **區域點擊互動**：點擊某個區域卡片時顯示彈出視窗，展示該區域的詳細資訊。
- **資料更新**：每 5 秒自動更新一次各區域長者的狀態，以確保即時性&#8203;:contentReference[oaicite:0]{index=0}。

## 資料庫

應用程式使用 SQLite 資料庫存儲用戶與長者資訊，包含以下資料表：
- `signdata`：存儲用戶註冊的基本資訊（例如 `firstname`、`lastname`、`username`、`password`）。
- `place104`、`place105`、`place106`：分別記錄不同編號長者的所在位置與時間。

## 樣式設計

- 樣式主要由 `main.css` 控制，用於定義整個頁面的佈局及樣式，例如卡片陰影、文字顏色、彈出視窗等&#8203;:contentReference[oaicite:1]{index=1}。

## 注意事項

- **開發環境**：本系統在本地測試，需在本地運行 Flask 伺服器。
- **通知功能**：需結合 Line Notify 完成通知功能。

## 系統要求

- Python 3.x
- Flask
- SQLite

## 開發者
- 此專案由林柏翰開發，歡迎進行改進與討論。
