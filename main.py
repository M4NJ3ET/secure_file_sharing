from fastapi import FastAPI
from app.routes import auth, ops_user, client_user

app = FastAPI()

app.include_router(auth.router)
app.include_router(ops_user.router)
app.include_router(client_user.router)