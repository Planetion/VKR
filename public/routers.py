from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.responses import JSONResponse
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

users_router = APIRouter(prefix='/api/users', tags=[Tags.user])
# level_router = APIRouter(prefix='/api/levels', tags=[Tags.level])

def coder_passwd(cod: str):
    return cod*2

#Поиск пользователя
@users_router.get("/{id}", response_model= Main_User, tags=[Tags.user])
def get_user(id: int, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.id == id).first()

    if user == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    else:
        return user

#Вывод всех пользователей
@users_router.get("/",response_model = list[Main_User] | None, tags=[Tags.user])
def get_user_db(db: Session = Depends(get_session)):
    users = db.query(User).all()
    if users == None:
        return JSONResponse(status_code=404, content={"message": " Пользователи не найдены"})
    return users

#Создание пользователя
@users_router.post("/", response_model= Main_User, status_code=status.HTTP_201_CREATED, tags=[Tags.user])
def create_user(item: Annotated[Main_User, Body(embed=True)],
                db: Session = Depends(get_session)):
    try:
        user = User(name=item.name, age = item.age)

        if user is None:
            raise HTTPException(status_code=404, detail="Объект не определён")
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при добавлении объекта {user}")

#Изменение пользователя
@users_router.put("/{id}", response_model = Main_User, tags=[Tags.user])
def edit_user(id: int, item: Annotated[Main_User, Body(embed=True)],
               db: Session = Depends(get_session)):
    user = db.query(User).filter(User.id == id).first()

    if user == None:
        return JSONResponse(status_code=404, content={"message":"Пользователь не найден"})
    user.name = item.name
    user.age = item.age
    try:
        db.commit()
        db.refresh(user)
    except HTTPException:
        return JSONResponse(status_code=404, content={"message": ""})
    return user

@users_router.patch("/{id}", response_model = Main_User, tags=[Tags.user])
def update_user(id: int, item: Annotated[Main_User, Body(embed=True)],
                db: Session = Depends(get_session)):
    user = db.query(User).filter(User.id == id).first()

    if user == None:
        return JSONResponse(status_code=404, content={"message":"Пользователь не найден"})
    if item.name != "string":
        user.name = item.name
    if item.age != 0:
        user.age = item.age
    try:
        db.commit()
        db.refresh(user)
    except HTTPException:
        return JSONResponse(status_code=404, content={"message": ""})
    return user

#Удаление пользователя
@users_router.delete("/{id}", response_class=JSONResponse, tags=[Tags.user])
def delete_user(id: int, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.id == id).first()

    if user == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    try:
        db.delete(user)
        db.commit()
    except HTTPException:
        return JSONResponse(content={'message': f'Ошибка'})
    return JSONResponse(content={'message': f'Пользователь удалён {id}'})


# #Поиск уровня
# @level_router.get("/{id}", response_model= Main_Level, tags=[Tags.level])
# def get_level(id: int, db: Session = Depends(get_session)):
#     level = db.query(Level).filter(Level.id == id).first()
#
#     if level == None:
#         return JSONResponse(status_code=404, content={"message": "Уровень не найден"})
#     else:
#         return level
#
# #Вывод всех уровней
# @level_router.get("/",response_model = list[Main_Level] | None, tags=[Tags.level])
# def get_level_db(db: Session = Depends(get_session)):
#     level = db.query(Level).all()
#     if level == None:
#         return JSONResponse(status_code=404, content={"message": " Уровни не найдены"})
#     return level
#
# #Создание уровня
# @level_router.post("/", response_model= Main_Level, status_code=status.HTTP_201_CREATED, tags=[Tags.level])
# def create_level(item: Annotated[Main_Level, Body(embed=True)],
#                 db: Session = Depends(get_session)):
#     try:
#         level = Level(size=item.size, body=item.body)
#         if level is None:
#             raise HTTPException(status_code=404, detail="Объект не определён")
#         db.add(level)
#         db.commit()
#         db.refresh(level)
#         return level
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Произошла ошибка при добавлении объекта {level}")
#
# #Изменение уровня
# @level_router.put("/{id}", response_model = Main_Level, tags=[Tags.level])
# def edit_level(id: int, item: Annotated[Main_Level, Body(embed=True)],
#                db: Session = Depends(get_session)):
#     level = db.query(Level).filter(Level.id == id).first()
#
#     if level == None:
#         return JSONResponse(status_code=404, content={"message":"Уровень не найден"})
#     level.size=item.size
#     level.body=item.body
#     try:
#         db.commit()
#         db.refresh(level)
#     except HTTPException:
#         return JSONResponse(status_code=404, content={"message": ""})
#     return level
#
# @level_router.patch("/{id}", response_model = Main_Level, tags=[Tags.level])
# def update_level(id: int, item: Annotated[Main_Level, Body(embed=True)],
#                 db: Session = Depends(get_session)):
#     level = db.query(Level).filter(Level.id == id).first()
#
#     if level== None:
#         return JSONResponse(status_code=404, content={"message":"Уровень не найден"})
#     if item.size != 0:
#         level.size = item.size
#     if item.body != "string":
#         level.body = item.body
#     try:
#         db.commit()
#         db.refresh(level)
#     except HTTPException:
#         return JSONResponse(status_code=404, content={"message": ""})
#     return level
#
# #Удаление уровня
# @level_router.delete("/{id}", response_class=JSONResponse, tags=[Tags.level])
# def delete_level(id: int, db: Session = Depends(get_session)):
#     level = db.query(Level).filter(Level.id == id).first()
#
#     if level == None:
#         return JSONResponse(status_code=404, content={"message": "Уровень не найден"})
#     try:
#         db.delete(level)
#         db.commit()
#     except HTTPException:
#         return JSONResponse(content={'message': f'Ошибка'})
#     return JSONResponse(content={'message': f'Уровень удалён {id}'})