# Pytest README

---

## Getting Started

### Create pytest.ini in **tests** directory

### Create custom argument as **conftest.py**

### Check what available mode in pytest

---

## Fixture

Fixture 是在測試中共用可以讓我們共用的資源，類似 Fast API 的 Depends

### Fixture Scope

1. function 每個測試 Function 都執行一次
2. class 每個測試 Class 都執行一次
3. module 每個測試 Module 都執行一次
4. session 整個測試都會執行一次
