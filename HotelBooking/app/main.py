from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import models, schemas, auth
from app.database import engine, SessionLocal
from app.dependencies import get_db


app = FastAPI(title="Hotel Booking System")

# -------- STARTUP --------
@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=engine)

# -------- ROOT (IMPORTANT) --------
@app.get("/")
def root():
    return {"status": "Hotel Booking API is running"}

# -------- MAINTENANCE MODE --------
@app.middleware("http")
async def maintenance(request: Request, call_next):
    db = SessionLocal()
    try:
        setting = db.query(models.SiteSetting).first()
        if setting and not setting.is_active:
            return JSONResponse(
                status_code=503,
                content={"message": "Website under maintenance"}
            )
        response = await call_next(request)
        return response
    finally:
        db.close()

# -------- AUTH --------
@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    u = models.User(
        name=user.name,
        email=user.email,
        password=auth.hash_password(user.password)
    )
    db.add(u)
    db.commit()
    return {"message": "User registered"}

@app.post("/login")
def login(data: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(email=data.email).first()
    if not user or not auth.verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token": auth.create_token({"sub": user.email})}

# -------- ROOMS --------
@app.post("/admin/room")
def add_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    db.add(models.Room(**room.dict()))
    db.commit()
    return {"message": "Room added"}

@app.get("/rooms")
def rooms(db: Session = Depends(get_db)):
    return db.query(models.Room).filter_by(is_available=True).all()

# -------- FEATURES --------
@app.post("/admin/feature")
def add_feature(data: schemas.FeatureCreate, db: Session = Depends(get_db)):
    db.add(models.RoomFeature(**data.dict()))
    db.commit()
    return {"message": "Feature added"}

# -------- SERVICES --------
@app.post("/admin/service")
def add_service(data: schemas.ServiceCreate, db: Session = Depends(get_db)):
    db.add(models.RoomService(**data.dict()))
    db.commit()
    return {"message": "Service added"}

# -------- BOOKING --------
@app.post("/book")
def book(data: schemas.BookingCreate, db: Session = Depends(get_db)):
    room = db.query(models.Room).filter(models.Room.id == data.room_id).first()
    if not room or not room.is_available:
        raise HTTPException(400, "Room not available")

    room.is_available = False
    db.add(models.Booking(user_id=1, **data.dict()))
    db.commit()
    return {"message": "Room booked"}

@app.post("/cancel/{booking_id}")
def cancel(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(404, "Booking not found")

    booking.status = "cancelled"
    room = db.query(models.Room).filter(models.Room.id == booking.room_id).first()
    room.is_available = True
    db.commit()
    return {"message": "Booking cancelled"}

# -------- REVIEW --------
@app.post("/review")
def review(data: schemas.ReviewCreate, db: Session = Depends(get_db)):
    db.add(models.Review(user_id=1, **data.dict()))
    db.commit()
    return {"message": "Review added"}

@app.get("/admin/reviews")
def reviews(db: Session = Depends(get_db)):
    return db.query(models.Review).all()

# -------- INVOICE --------
@app.post("/admin/invoice/{booking_id}")
def invoice(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(404, "Booking not found")

    room = db.query(models.Room).filter(models.Room.id == booking.room_id).first()
    inv = models.Invoice(
        booking_id=booking_id,
        amount=room.price,
        status="paid"
    )
    db.add(inv)
    db.commit()
    return inv

# -------- SHUTDOWN --------
@app.post("/admin/shutdown")
def shutdown(db: Session = Depends(get_db)):
    s = db.query(models.SiteSetting).first()
    if not s:
        s = models.SiteSetting(is_active=False)
        db.add(s)
    else:
        s.is_active = False
    db.commit()
    return {"message": "Website shutdown"}

@app.post("/admin/start")
def start(db: Session = Depends(get_db)):
    s = db.query(models.SiteSetting).first()
    if not s:
        s = models.SiteSetting(is_active=True)
        db.add(s)
    else:
        s.is_active = True
    db.commit()
    return {"message": "Website started"}
