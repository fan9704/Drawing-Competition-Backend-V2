from typing import List,Type, TypeVar
from abc import ABC, abstractmethod
from tortoise import models

T = TypeVar("T", bound=models.Model)

class Repository(ABC):
    model: Type[T]
    # 初始化 給定 ORM 操作目標
    @abstractmethod
    def __init__(self, model:T) -> None:
        raise NotImplementedError()

    # 建立物件
    async def create(self, **data) -> T:
        obj = await self.model.create(**data)
        return obj

    # 新增多筆資料
    async def bulk_create(self, objs):
        return await self.model.bulk_create(objs)

    # 儲存
    async def save(self, obj):
        await self.model.save(obj)

    # 刪除 ID 資料
    async def delete_by_id(self, pk: int):
        return await self.model.filter(id=pk).delete()

    # 刪除資料
    async def delete_object(self, obj):
        return await obj.delete()

    # 單筆查詢
    async def get_by_id(self, pk)->T:
        return await self.model.get(pk=pk)

    # 多筆查詢
    async def find_all(self) -> List[T]:
        return await self.model.all()

    # 過濾
    async def filter(self,**params)->List[T]:
        return await self.model.filter(**params)