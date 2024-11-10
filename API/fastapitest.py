from typing import Union
from fastapi import FastAPI #for get
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

"""web gui for api testing
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
"""

#--------------------------------------------------------------------------------------------------------------------- GET - Retrieval 

#--------------------------------------------------------- for http://127.0.0.1:8000/

@app.get("/")
def read_root():
    return {"Hello": "World"}

#--------------------------------------------------------- for http://127.0.0.1:8000/items/5?q=somequery <= this string ("somequery" in this case) is passed to q
#                                                                                         /\   
#                                                                                         ||      
#                                                                       this int (5 in this case) passed to item_id 



@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None): #item_id can only be int, q can either be a str or a None value and q defaults to None if no string is provided 
    return {"item_id": item_id, "q": q}

"""inputs/outputs
http://127.0.0.1:8000/items/?q=somequery prints {"detail":"Not Found"}
http://127.0.0.1:8000/items/5? prints {"item_id":5,"q":null}
This is because q can be null as our code above describes but item_id cannot be null here"""

#--------------------------------------------------------------------------------------------------------------------- PUT - Updation

class Item(BaseModel): #dw about BaseModel, unrelated to fast api but to put it simply, class named Item with with 3 attributes
    name: str
    price: float
    is_offer: Union[bool, None] = None

#--------------------------------------------------------- for http://127.0.0.1:8000/items/13 <= this int ( 13 in this case) passed to item_id but notice that Item, the object, is not passed here 

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id, "item_price": item.price, "item_is_offer": item.is_offer}