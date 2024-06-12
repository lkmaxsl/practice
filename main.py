from fastapi import FastAPI,Query
from typing import Optional
from pydantic import BaseModel


class item(BaseModel):
    name:str
    description:Optional[str]=None #one way to do a optional 
    price:float
    tax:float | None = None #another way to do a optional

app = FastAPI()


@app.get("/")
def get_inf():
    return {"message":"Hello"}

#path parameters 
@app.get("/item/{itemid}")
def get_1(itemid:int):
    return {"item id": itemid}

#queary parameters

@app.get("/item/{itemid}")
def get_2(itemid:str):
    pass



@app.get("user/{userid}/item/{itemid}")
def get_userid(userid:int,):
    pass

@app.post("/")
def post_info():
    return {"message":"world"}

@app.post("/item")
def create_item():
    return item

@app.get("/item")
def read_item(q:str = Quary(...,min_length = 3, max_length = 10)):
    results = {"items": [{"items id":"Foo"},{"items id":"Bar"}]}
    if q:
        results.update({"q":q})
        return results
    
@app.get ("/item_validate/item_id")
def reat_item_validation(item_id:int = path (...,title="the 10 of the item to get"),q: str):
    results = {"item_id":item_id}
    if q:
        results.update({"q": q})