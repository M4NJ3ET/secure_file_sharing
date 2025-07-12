from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, database
from passlib.context import CryptContext
import uuid

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# DB session dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Password Hash
def hash_password(password: str):
    return pwd_context.hash(password)

# Password Verify
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# SIGNUP ROUTE
@router.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    new_user = models.User(
        email=user.email,
        password=hashed_pw,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    encrypted_url = f"/download-file/{uuid.uuid4()}"

    return {
        "message": "Signup successful. Email verification pending.",
        "encrypted_download_url": encrypted_url
    }

# LOGIN ROUTE
@router.post("/login")
def login(form_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")

    return {
        "message": "Login successful",
        "user_id": user.id,
        "role": user.role
    }
