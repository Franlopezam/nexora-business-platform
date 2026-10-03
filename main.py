from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings
from .database import init_db
from .middleware.rate_limit import SimpleRateLimitMiddleware
from .routers import auth, products, customers, sales, inventory, dashboard, reports, audit

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Nexora business management API",
)

app.add_middleware(SimpleRateLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(customers.router)
app.include_router(sales.router)
app.include_router(inventory.router)
app.include_router(dashboard.router)
app.include_router(reports.router)
app.include_router(audit.router)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/api/health")
def health():
    return {"status": "ok", "service": settings.app_name}


frontend = Path(__file__).resolve().parents[2] / "frontend"
app.mount("/", StaticFiles(directory=frontend, html=True), name="frontend")
