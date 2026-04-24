from pydantic import BaseModel



class UserCreate (BaseModel):
    username: str
    email: str
    password: str


class Userlogin (BaseModel):
    username: str
    password: str


class ProductCreate (BaseModel):
    name: str
    description: str
    price: float
    condition: str
    category_id: int


