from fastapi import FastAPI
from typing import List, TypedDict
from connection import init_db

from models import Warrior

app = FastAPI()

# Простое API без валидации данных
@app.get("/")
def hello():
    return "Hello, [username]!"

"""
Первая версия временной бд
temp_bd = [{
    "id": 1,
    "race": "admin",
    "name": "Мартынов Дмитрий",
    "level": 12,
    "profession": {
        "id": 1,
        "title": "Влиятельный человек",
        "description": "Эксперт по всем вопросам"
    },
},
    {
        "id": 2,
        "race": "moderator",
        "name": "Андрей Косякин",
        "level": 12,
        "profession": {
            "id": 1,
            "title": "Дельфист-гребец",
            "description": "Уважаемый сотрудник"
        },
    },
]
"""

# Вторая версия temp_bd
temp_bd = [
{
    "id": 1,
    "race": "admin",
    "name": "Мартынов Дмитрий",
    "level": 12,
    "achievements": {
        "id": 1,
        "title": "Влиятельный человек",
        "description": "Add first book"
    },
    "books":
        [{
            "id": 1,
            "name": "1984",
            "description": "George Orwell"

        },
        {
            "id": 2,
            "name": "The Picture of Dorian Gray",
            "description": "Oscar Fingal O'Flahertie Wills Wilde"

        }]
},
{
    "id": 2,
    "race": "moderator",
    "name": "Андрей Косякин",
    "level": 12,
    "achievements": {
        "id": 1,
        "title": "Дельфист-гребец",
        "description": "Выполните первую проверку топика"
    },
    "books": []
},
]


@app.get("/warriors_list")
def warriors_list() -> List[Warrior]:
    return temp_bd


@app.get("/warrior/{warrior_id}")
def warriors_get(warrior_id: int) -> List[Warrior]:
    return [warrior for warrior in temp_bd if warrior.get("id") == warrior_id]


@app.post("/warrior")
def warriors_create(warrior: Warrior) -> TypedDict('Response', {"status": int, "data": Warrior}):
    warrior_to_append = warrior.model_dump()
    temp_bd.append(warrior_to_append)
    return {"status": 200, "data": warrior}


@app.delete("/warrior/delete{warrior_id}")
def warrior_delete(warrior_id: int):
    for i, warrior in enumerate(temp_bd):
        if warrior.get("id") == warrior_id:
            temp_bd.pop(i)
            break
    return {"status": 201, "message": "deleted"}


@app.put("/warrior{warrior_id}")
def warrior_update(warrior_id: int, warrior: Warrior) -> List[Warrior]:
    for war in temp_bd:
        if war.get("id") == warrior_id:
            warrior_to_append = warrior.model_dump()
            temp_bd.remove(war)
            temp_bd.append(warrior_to_append)
    return temp_bd

@app.on_event("startup")
def on_startup():
    init_db()
