from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.logging_config import configure_logging
from app.core.middleware import RequestIDMiddleware
from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler,
)
from app.database import init_db
from app.routers import (
    auth_router, campaign_router, contact_router,
    send_router, tracking_router, stats_router
)

configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Email Campaign Tracker",
    description="Manage campaigns, contacts, and email tracking in one API.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(RequestIDMiddleware)

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.include_router(auth_router.router)
app.include_router(campaign_router.router)
app.include_router(contact_router.router)
app.include_router(send_router.router)
app.include_router(tracking_router.router)
app.include_router(stats_router.router)


@app.get('/health')
async def health():
    return {
        'Status': 'Ok',
        'db_connected': True,
    }
    
    