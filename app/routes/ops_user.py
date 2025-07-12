from fastapi import APIRouter, UploadFile, File, HTTPException, File, Depends
from sqlalchemy.orm import Session
from app import models,schemas
from app.database import get_db
from passlib.context import CryptContext
import os
from datetime import datetime  

router = APIRouter(
    prefix="/ops",
    tags=["Ops User"]
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

UPLOAD_DIR = "ops_uploaded_files"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


# Example route (placeholder)
@router.get("/test")
def test_ops():
    return {"message": "Ops route working"}




@router.post("/login")
def ops_login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if db_user.role != models.RoleEnum.OPS:
        raise HTTPException(status_code=403, detail="Not authorized as Ops User")

    return {"message": "Login successful", "user": db_user.email}



@router.post("/upload-file/{email}")
def upload_ops_file(email: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    allowed_types = [
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",  # .pptx
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",     # .docx
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"            # .xlsx
    ]

    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Only pptx, docx, xlsx files are allowed")

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{email}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return {"message": "File uploaded by Ops User", "filename": filename}


