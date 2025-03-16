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

## Reference

1. [pytest测试框架中的setup和tearDown](https://python012.github.io/2018/05/08/pytest%E6%B5%8B%E8%AF%95%E6%A1%86%E6%9E%B6%E4%B8%AD%E7%9A%84setup%E5%92%8CtearDown/)