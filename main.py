from fastapi import FastAPI,Query,Path
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


'''Part 7 -  Multiple Parameters'''

class Item(BaseModel):
    name : str
    description : str | None = None
    price : float
    tax : float | None = None

class User(BaseModel):
    username : str
    full_bane : str | None = None

'''
@app.put("/item/{item_id}")
def update_item(
    item_id: int=path(...,title="The id of the item to get", get=0,le=150),
    q:str | None =None,
    item : Item | None = None
    user:User,
    importance : int
):
    results = {"item_id" : item_id}
    if q:
        results.update({"q":q})
    if item:
        results.update({"item":item})
    if User:
        results.update({"user": User})
    if impotance:
        results.update({"imortance" : importance})

    return results
    '''

@app.put ("/items/{item_id}")
def update_item(
    item_id : int
    item:Item = Body(
        ...,
        examples={
            "summary": "A normalexample",
            "description": "A __normal__ item works _correctly_",
            "value":{"name": "Foo",
                      "description": "A very nice Item"
                      "price" : 16.25,
                      "tax": 1.67,
                      },
        },
        "converted": {
            "summary": "An example with converted date",
            "description": "FastAPI can convert price 'strings' to"
            "value": {"name":"Bar","price":"16.25"},

        },
        "invalid": {
            "summary": "Invalid date is rejected with an error",
            "description": "Hello youtubers",
            "value": {"name":"Baz", "price": "sixteen point two five"}
        },
    )

): 
    results= {"item_id":item_id, "item":item}
    return results
