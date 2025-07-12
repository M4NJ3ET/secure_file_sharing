from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from passlib.context import CryptContext
from cryptography.fernet import Fernet
import os
from datetime import datetime





router = APIRouter(
    prefix="/client",
    tags=["Client User"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from dotenv import load_dotenv
load_dotenv()

key = os.getenv("FERNET_KEY").encode()
fernet = Fernet(key)

@router.post("/signup")
def client_signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user.password)
    new_user = models.User(
        email=user.email,
        password=hashed_password,
        role=models.RoleEnum.CLIENT
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate encrypted download URL
    encrypted_id = fernet.encrypt(str(new_user.id).encode()).decode()
    download_url = f"http://127.0.0.1:8000/client/download-file/{encrypted_id}"

    return {
        "message": "Signup successful. Verification mail sent (simulated)",
        "encrypted-download-url": download_url
    }



@router.get("/test")
def test_client(db: Session = Depends(get_db)):
    return {"message": "Client route working fine ✅"}


UPLOAD_DIR = "client_uploaded_files"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/upload-file/{email}")
def upload_client_file(email: str, file: UploadFile = File(...)):
    allowed_types = [
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",  # .pptx
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",     # .docx
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"            # .xlsx
    ]

    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Only pptx, docx, xlsx files are allowed")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{email}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return {"message": "Client file uploaded successfully", "filename": filename}



from fastapi.responses import FileResponse

@router.get("/download-file/{encrypted_id}")
def download_file(encrypted_id: str, db: Session = Depends(get_db)):
    try:
        user_id = int(fernet.decrypt(encrypted_id.encode()).decode())
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or expired download link")

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get all files in the upload folder
    files = os.listdir(UPLOAD_DIR)

    # Match files uploaded by this user (based on ID in filename)
    user_files = [f for f in files if f.endswith(f"_{user.email}")]

    if not user_files:
        raise HTTPException(status_code=404, detail="No files uploaded by this user")

    latest_file = sorted(user_files)[-1]
    file_path = os.path.join(UPLOAD_DIR, latest_file)

    return FileResponse(path=file_path, filename=latest_file, media_type='application/octet-stream')




@router.get("/list-files/{email}")
def list_client_files(email: str):
    if not os.path.exists(UPLOAD_DIR):
        raise HTTPException(status_code=404, detail="No files uploaded yet")

    files = os.listdir(UPLOAD_DIR)
    user_files = [f for f in files if f.endswith(f"_{email}")]

    if not user_files:
        raise HTTPException(status_code=404, detail="No files found for this user")

    return {"files": user_files}


#GET http://127.0.0.1:8000/client/list-files/someone@example.com
