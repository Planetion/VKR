from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette import status
from sqlalchemy.orm import Session
from models.tables import *
from models.shemes import *
from db import engine
from typing import Annotated

def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()

level_router = APIRouter(prefix='/api/levels', tags=[Tags.level])

#Поиск уровня
@level_router.get("/{id}", response_model=Main_Data, tags=[Tags.level])
def get_level(id: int, db: Session = Depends(get_session)):
    level = db.query(Data).filter(Data.lvl_id == id).first()

    if level == None:
        return JSONResponse(status_code=404, content={"message": "Уровень не найден"})
    else:
        return level

#Вывод всех уровней
@level_router.get("",response_model=list[Main_Data] | None, tags=[Tags.level])
def get_level_db(db: Session = Depends(get_session)):
    level = db.query(Data).all()
    if level == None:
        return JSONResponse(status_code=404, content={"message": " Уровни не найдены"})
    return level

#Создание уровня
@level_router.post("/", response_model=Main_Data, status_code=status.HTTP_201_CREATED, tags=[Tags.level])
def create_level(item: Annotated[Main_Data, Body(embed=True)],
                 db: Session = Depends(get_session)):
    try:
        level_data = Data(size=item.size, body=item.body,
                          start_x=item.start_x, start_y=item.start_y,
                          end_x=item.end_x, end_y=item.end_y)
        level = Level(data=level_data)
        if level is None:
            raise HTTPException(status_code=404, detail="Объект не определён")
        db.add(level)
        db.commit()
        db.refresh(level)
        return JSONResponse(content=jsonable_encoder(level))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при добавлении объекта {level}")

#Изменение уровня
@level_router.put("/{id}", response_class = Main_Data, tags=[Tags.level])
def edit_level(id: int, item: Annotated[Main_Data, Body(embed=True)],
               db: Session = Depends(get_session)):
    level = db.query(Data).filter(Data.lvl_id == id).first()

    if level == None:
        return JSONResponse(status_code=404, content={"message":"Уровень не найден"})
    level.size = item.size
    level.body = item.body
    level.start_x = item.start_x
    level.start_y = item.start_y
    level.end_x = item.end_x
    level.end_y = item.end_y
    try:
        db.commit()
        db.refresh(level)
    except HTTPException:
        return JSONResponse(status_code=404, content={"message": ""})
    return level

@level_router.patch("/{id}", response_model=Main_Data, tags=[Tags.level])
def update_level(id: int, item: Annotated[Main_Data, Body(embed=True)],
                db: Session = Depends(get_session)):
    level = get_level(id, db)

    if level== None:
        return JSONResponse(status_code=404, content={"message":"Уровень не найден"})
    if item.size != level.size:
        level.size = item.size
    if item.body != level.body:
        level.body = item.body
    if item.start_x != level.start_x:
        level.start_x = item.start_x
    if item.start_y != level.start_y:
        level.start_y = item.start_y
    if item.end_x != level.end_x:
        level.end_x = item.end_x
    if item.end_y != level.end_y:
        level.end_y = item.end_y
    try:
        db.commit()
        db.refresh(level)
    except HTTPException:
        return JSONResponse(status_code=404, content={"message": ""})
    return level

#Удаление уровня
@level_router.delete("/{id}", response_class=JSONResponse, tags=[Tags.level])
def delete_level(id: int, db: Session = Depends(get_session)):
    level = db.query(Level).filter(Level.id == id).first()

    if level == None:
        return JSONResponse(status_code=404, content={"message": "Уровень не найден"})
    try:
        db.delete(level)
        db.commit()
    except HTTPException:
        return JSONResponse(content={'message': f'Ошибка'})
    return JSONResponse(content={'message': f'Уровень удалён {id}'})

# @level_router.put("/{id}/start", response_class= JSONResponse, tags=[Tags.level])
# def edit_start(id: int, item: Annotated[Main_Start_Point, Body(embed=True)],
#                db: Session = Depends(get_session)):
#     point = db.query(Level).filter(Level.id == id).first()
#
#     if point == None:
#         return JSONResponse(status_code=404, content={"message":"Уровень не найден"})
#     point.start_x = item.start_x
#     point.start_y = item.start_y
#     try:
#         db.commit()
#         db.refresh(point)
#     except HTTPException:
#         return JSONResponse(status_code=404, content={"message": ""})
#     return point
#
# @level_router.put("/{id}/end", response_model = Main_End_Point, tags=[Tags.level])
# def edit_end(id: int, item: Annotated[Main_End_Point, Body(embed=True)],
#                db: Session = Depends(get_session)):
#     point = db.query(Level).filter(Level.id == id).first()
#
#     if point == None:
#         return JSONResponse(status_code=404, content={"message":"Уровень не найден"})
#     point.end_x = item.end_x
#     point.end_y = item.end_y
#     try:
#         db.commit()
#         db.refresh(point)
#     except HTTPException:
#         return JSONResponse(status_code=404, content={"message": ""})
#     return point