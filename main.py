from enum import Enum

from typing import Annotated

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel


class AnimalName(str, Enum):
    snake = "snake"
    frog = "frog"
    sheep = "sheep"


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: int, grumpy: str):
    item = {"user_id": user_id, "grumpy": grumpy}
    return item


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
async def read_items(
    skip: int = 0,
    limit: int = 10,
    q: Annotated[
        str | None,
        Query(min_length=3, max_length=50, pattern="^fixedquery$", alias="item-query"),
    ] = None,
    # can use other defaults;
    # skipping the default here make the parameter required;
    # parameter can be of type None and still be required
):
    if q:
        fake_items_db.update({"q": q})
    return fake_items_db[skip : skip + limit]


# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: str | None = None, short: bool = False):
#    item = {"item_id": item_id}
#    if q:
#        item.update({"q": q})
#    if not short:
#        item.update({"description": "A long description for an item from the list."})
#
#    return item

# ---- Path parameters and numeric validations -----


@app.get("/items/{item_id}")
async def read_item(
    # declare parameters as kwargs to have your prefered order
    *,
    item_id: int = Path(title="The id of an item to get"),
    q: str,
):
    results = {"item_id": item_id}
    if q:
        results.q = q
    return results


@app.post("/items")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result


# defining a parameter with multiple values
@app.get("/examples")
async def read_examples(q: Annotated[list[str] | None, Query(deprecated=True)] = None):
    query_examples = {"q": q}
    return query_examples
