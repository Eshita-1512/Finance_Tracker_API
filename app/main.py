from http import HTTPStatus
from app.routers import auth,transactions,summary,admin
from fastapi import FastAPI,APIRouter

app = FastAPI()

app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(summary.router)
app.include_router(admin.router)

app.get("/health")
def health_check():
    if(HTTPStatus.OK == 200):
        return {"status": "ok"}
    else:
        return {"status": "error"}






