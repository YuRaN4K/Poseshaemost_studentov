import uvicorn
from fastapi import FastAPI
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configurations
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# SQLAlchemy models
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(String, index=True)
    description = Column(String, index=True)


Base.metadata.create_all(bind=engine)

# FastAPI main
app = FastAPI()


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
@app.get("/items/ids/by-date")
async def read_ids_by_date(date: str = None):
    db = SessionLocal()
    try:
        if date:
            # Возвращает список ID только для конкретной даты
            items = db.query(Item.id).filter(Item.date == date).all()
            # Преобразуем список кортежей [(1,), (2,)] в плоский список [1, 2]
            return {date: [item[0] for item in items]}
        
        # Если дата не указана, возвращаем все существующие пары Дата: [ID, ID...]
        all_items = db.query(Item.id, Item.date).all()
        result = {}
        for item_id, item_date in all_items:
            if item_date not in result:
                result[item_date] = []
            result[item_date].append(item_id)
        return result
    finally:
        db.close()



if __name__ == "__main__":
    uvicorn.run(app)