from http import HTTPStatus
from app.routers import auth,transactions,summary,admin
from fastapi import FastAPI,APIRouter

from fastapi.responses import RedirectResponse

import traceback
from fastapi import Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        # Print the traceback in the console (shows up in Render logs)
        print(f"--- INTERNAL ERROR ---\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error", "error_info": str(e)},
        )

app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(summary.router)
app.include_router(admin.router)

@app.get("/")
def main_root():
    print("Health check: root reached")
    return RedirectResponse(url="/docs")

@app.get("/health")
def health_check():
    return {"status": "ok"}






