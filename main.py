from fastapi import FastAPI,Query,Path,Body,Cookie,Header,status,Form,File,HTMLResponse
from typing import Optional, Literal,Union
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from uuid import UUID
from datetime import datetime, time, timedelta

app = FastAPI()

'''
class item(BaseModel):
    name:str
    description:Optional[str]=None #one way to do a optional 
    price:float
    tax:float | None = None #another way to do a optional

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


Part 7 -  Multiple Parameters

class Item(BaseModel):
    name : str
    description : str | None = None
    price : float
    tax : float | None = None

class User(BaseModel):
    username : str
    full_bane : str | None = None


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

part 11 - Extra Data Types

@app.put ("/items/{item_id}")
def read_items(
    item_id:UUID, 
     start_date:datetime| None = Body(None), 
    end_date:datetime |None = Body(None),
    repeat_at: time|None = Body(None),
    process_after: timedelta | None = Body(None),
    ):
    
    start_process = start_date + process_after
    duration = end_date - start_process

    return {
        "item_id":item_id,
        "start_date":start_date,
        "end_date":end_date,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
        }

part 12 - Cookie and Header Parameters



@app.get("/items")
def read_items(
    cookie_id: str |None=Cookie(None),
    accept_encoding: str|None=Header(None, convert_underscores=False),
    sec_ch_ua:str|None=Header(None),
    user_agent: str|None=Header(None),

):
    return {
        "cookie_id": cookie_id,
        "Accept_Encoding": accept_encoding,
        "sec-ch-ua":sec_ch_ua,
        "User-Agent":user_agent
        }


part 13 - Response Model    

class Item(BaseModel):
    name:str
    description:str | None=None
    price:float
    tax:float =10.5
    tags: list[str]=[]
items = {
    "foo":{"name":"Foo","price":50.2},
    "bar":{"name":"Bar ", "description":"The bartenders","price":62, "tax":20.2},
    "baz":{"name":"Baz ", "description":None,"price":50.2, "tax":10.5,"tags":[]},
}

@app.get("/items/{item_id}", response_model=Item,response_model_exclude_unset=True)
def read_item(item_id: Literal["foo","bar","baz"]):
    return items[item_id]


@app.post("/items", response_model=Item)
def create_item(item:Item):
    return item

class UserBase(BaseModel):
    username:str
    email: EmailStr
    full_name: str | None=None 

class UserIn(UserBase):
     password:str

class UserOut(UserBase):
    pass


@app.post("/user", response_model=UserOut)
def create_user(user:UserIn):
    return user

@app.get(
        "/items/{item_id}/name",
        response_model=Item,
        response_model_include={"name""description"}
        )
def read_item_name(item_id: Literal['foo','bar','baz']):
    return items[item_id]

@app.get(
        "/items/{item_id}/public",
         response_model=Item,
         response_model_exclude={"tax"}
         )
def read_item_public_data(item_id: Literal['foo','bar','baz']):
    return items[item_id]

Part 14 - Extra Models
   
class UserBase(BaseModel):
    username:str
    password:str
    email: EmailStr
    full_name: str | None=None

class UserIn(UserBase):
    password:str

class UserOut(UserBase):
   pass

class UserInDB(UserBase):
    hashed_password:str
  
def fake_password_hasher(raw_password: str):
    return f"supersecret{raw_password}"

   
def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("UserIn.dict", user_in.dict())
    print("user saved")
    print("user saved")
    return user_in_db

@app.post("/user",response_model=UserOut)
def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

class BaseItem(BaseModel):
    description:str
    type:str

class CarItem(BaseItem):
    type = "car"

class PlaneItem(BaseItem):
    type = "plane"
    size: int

items = {
    "item1":{"description": "All my friends drive a low rider", "type": "car"},
    "item2":{"description": "Music is my aeroplane, it's my aeroplane","type": "plane","size":5},
}

@app.get("/items/{item_id}",response_model=Union[PlaneItem,CarItem])
def read_item(item_id: Literal["item1","item2"]):
    return items[item_id]

class ListItem(BaseModel):
    name:str
    description:str

list_items = [
    {"name":"Foo","description":"there comes my hero"},
    {"name":"Red","description":"It's my aeroplane"}
]

app.get("/list_items",response_model=list[ListItem])
def read_items():
    return items

app.get("/arbitrary",response_model=dict[str,float])
def get_arbitrary():
    return {"Foo":1,"bar":2}

Part 15 - Response Status Codes

@app.post("/items", status_code=201)
def crate_item(name: str):
    return {"name":name}

@app.post("/items", status_code=status.HTTP_201_CREATED)
def crate_item2(name: str):
    return {"name":name}

@app.delete("/items/{pk}", status_code=status.HTTP_204_NO_CONTENT)
def delet_item(pk: str):
    print("pk",pk)
    return pk

@app.get("/items", status_code=status.HTTP_302_FOUND)
def read_items_redirect():
    return {"hello":"world"}

part 16- Form Fields

@app.post("login")
def login(username:str = Form(...),password:str=form(...)):
    print("password",password)
    return {"username": username}

class User(BaseModel):
    username:str
    password:str

@app.post ("/login-json")
def login_json(username:str=Body(...), password: str=Body(...)):
    print("password",password)
    return {"username":username}
    
Part 17 - Request Files (upload a file)
'''

@app.post("/files")
def create_file(files: bytes | None=File(None, description="A file read as bytes")):
    if not files:
        return {"message":"No file sent"}
    return{"file": [len(file) for file in files]}

@app.post("/uploadfile")
def create_upload_file(files: list[uploadFile]=File(..., description="A file read as uploadFile")):
    return{"filename": [file.filename for file in files]}

@app.get("/")
def main():
    content = """
<body>
<form action = "/files" encrype = "multipart/form-data" method = "post">
<input name = "files" type = "file" multiple>
<input type = "submit">
</form>
<form action="/uploadfiles" enctype="multipart/form-data" method="post">
<input name = "files" type = "file" multiple>
<input type="submit">
</form>
</body>

"""
    return HTMLResponse(content=content)
