from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# Модель данных для заметки
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    completed: bool = False
    description: Optional[str] = None
    

# Имитация бд в оперативке
db = [
    {"id": 1, "name": "Имя студента","completed": False, "description": "причина неявки"}
]

# 1. READ (Получить список всех элементов)
@app.get("/items", response_model=List[Item])
def get_items():
    return db

# CREATE (Добавить новый элемент)
@app.post("/items", response_model=Item)
def create_item(item: Item):
    item.id = len(db) + 1
    db.append(item.dict())
    return item

# READ (Получить один элемент по ID)
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    for item in db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# UPDATE (Обновить существующий элемент)
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(db):
        if item["id"] == item_id:
            updated_item.id = item_id
            db[index] = updated_item.dict()
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

# DELETE (Удалить элемент)
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for index, item in enumerate(db):
        if item["id"] == item_id:
            db.pop(index)
            return {"message": f"Item {item_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")
