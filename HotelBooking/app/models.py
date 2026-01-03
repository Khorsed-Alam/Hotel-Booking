from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Date
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)
    is_banned = Column(Boolean, default=False)

class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True)
    room_number = Column(String, unique=True)
    price = Column(Float)
    is_available = Column(Boolean, default=True)

class RoomFeature(Base):
    __tablename__ = "room_features"
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    feature = Column(String)

class RoomService(Base):
    __tablename__ = "room_services"
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    service = Column(String)

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    check_in = Column(Date)
    check_out = Column(Date)
    status = Column(String, default="booked")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    room_id = Column(Integer)
    rating = Column(Integer)
    comment = Column(String)

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer)
    amount = Column(Float)
    status = Column(String)

class SiteSetting(Base):
    __tablename__ = "site_settings"
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean, default=True)
