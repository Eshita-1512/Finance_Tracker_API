from http import HTTPStatus
from app.routers import auth,transactions,summary,admin
from fastapi import FastAPI,APIRouter

from fastapi.responses import RedirectResponse

app = FastAPI()

app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(summary.router)
app.include_router(admin.router)

@app.get("/")
def main_root():
    return RedirectResponse(url="/docs")

@app.get("/health")
def health_check():
    return {"status": "ok"}






