from fastapi import APIRouter
from src.models.tortoise import Item as TItem
from src.models.pydantic import Item

router = APIRouter()


@router.post("/", description="Create a new item")
async def post(item: Item):
    i = await TItem.create(**item.dict())
    await i.save()
    return {"response": "Successfully created new one"}


@router.get("/", summary="Get All Items", description="Get all items", response_description="All Items")
async def get() -> list[Item]:
    items = await TItem.all()
    return items
