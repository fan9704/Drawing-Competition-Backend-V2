from tortoise import models


class Repository:
    # 初始化 給定 ORM 操作目標
    def __init__(self, model: models.Model):
        self.model = model

    # 建立物件
    async def create(self, **data):
        obj = await self.model.create(**data)
        return obj

    # 新增多筆資料
    async def bulk_create(self, objs):
        return await self.model.bulk_create(objs)

    # 儲存
    async def save(self, obj):
        return await self.model.save(obj)

    # 刪除 ID 資料
    async def delete_by_id(self, pk: int):
        return await self.model.filter(id=pk).delete()

    # 刪除資料
    async def delete_object(self, obj):
        return await obj.delete()

    # 單筆查詢
    async def get_by_id(self, pk):
        return await self.model.get(pk=pk)

    # 多筆查詢
    async def find_all(self):
        return await self.model.all()

    # 過濾
    async def filter(self):
        return await self.model.filter()