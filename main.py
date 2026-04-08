from enum import Enum

from fastapi import FastAPI


class AnimalName(str, Enum):
    snake = "snake"
    frog = "frog"
    sheep = "sheep"


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id}


@app.get("/animals/{animal_name}")
async def get_animal(animal_name: AnimalName):
    if animal_name is AnimalName.frog:
        return {"animal_name": animal_name, "message": "kum, kum"}
    if animal_name is AnimalName.snake:
        return {"animal_name": animal_name, "message": "ssssssss..."}

    return {"animal_name": animal_name, "message": "meeeeee..."}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


@app.get("/items")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
