import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List, Optional, Dict, Any

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(String, index=True)
    description = Column(String, index=True)

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoints:
# Create
@app.post("/items/")
async def create_item(name: str,date: str ,description: str):
    db = SessionLocal()
    db_item = Item(name=name, date=date ,description=description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# Read
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()
    return item


# Update
@app.put("/items/{item_id}")
async def update_item(item_id: int, name: str, date: str ,description: str):
    db = SessionLocal()
    db_item = db.query(Item).filter(Item.id == item_id).first()
    db_item.name = name
    db_item.date = date
    db_item.description = description
    db.commit()
    return db_item


# Delete
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    db = SessionLocal()
    db_item = db.query(Item).filter(Item.id == item_id).first()
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully"}



# Read all IDs grouped by date or filtered by date
@app.get("/items/info/by-date")
async def read_items_info_by_date(date: Optional[str] = None, db: Session = Depends(get_db)):

    if date:
        # Если дата указана: возвращаем плоский список [{}, {}]
        items = db.query(Item.name, Item.description).filter(Item.date == date).all()
        return [{"name": item.name, "description": item.description} for item in items]
    else:
        # Если дата не указана то выводится все даты
        all_items = db.query(Item.name, Item.description, Item.date).all()
        result = {}
        for item_name, item_description, item_date in all_items:
            if item_date not in result:
                result[item_date] = []
            result[item_date].append({
                "name": item_name,
                "description": item_description
            })
        return result



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)