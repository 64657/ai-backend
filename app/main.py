from fastapi import FastAPI
from app.routes.users import router as users_router
from app.routes import auth
from app.routes import documents

app = FastAPI()

app.include_router(users_router)

app.include_router(auth.router)

app.include_router(documents.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}