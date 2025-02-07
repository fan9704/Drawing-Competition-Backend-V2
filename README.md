# Drawing Competition Backend

Refactor Version by FastAPI

---

- [Swagger] - 127.0.0.1:8000/docs

---

## Getting Start

### Install Dependencies

```shell
poetry install
poetry shell
```

### Set Postgres Timezone as Taiwan

```shell
ALTER DATABASE your_database SET TIMEZONE TO 'Asia/Taipei';
```

### Install in Server Global Environment

```shell
# GhostScript
pip install requests psutil opencv-python sentence-transformers pillow
```

### Run Server

```shell
uvicorn src.main:app --reload
```