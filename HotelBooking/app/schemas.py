from pydantic import BaseModel
from datetime import date

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str

class RoomCreate(BaseModel):
    room_number: str
    price: float

class FeatureCreate(BaseModel):
    room_id: int
    feature: str

class ServiceCreate(BaseModel):
    room_id: int
    service: str

class BookingCreate(BaseModel):
    room_id: int
    check_in: date
    check_out: date

class ReviewCreate(BaseModel):
    room_id: int
    rating: int
    comment: str
