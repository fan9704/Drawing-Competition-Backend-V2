# Python 繪圖大挑戰-後端  V2

Refactor Version by FastAPI

---

- [Swagger] - 127.0.0.1:8000/docs

---

## 開始遊玩


###

---

## 開始入手

### 安裝依賴

```shell
poetry install
poetry shell
```

### 設置 PostgresSQL 時區

```shell
ALTER DATABASE your_database SET TIMEZONE TO 'Asia/Taipei';
```

### 在伺服器端安裝以下依賴(全域)

```shell
# GhostScript
pip install requests psutil opencv-python sentence-transformers pillow
```

### 啟動伺服器

```shell
uvicorn src.main:app --reload
```