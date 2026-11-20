from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import create_tables
from routes.reviews import router as reviews_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables before the application starts serving requests."""
    create_tables()
    print("DB tables are being created...")
    yield
    # Run cleanup tasks here when application shutdown behavior is added.
    print("Application is shutting down...")


# Create the FastAPI application and expose review endpoints.
app = FastAPI(
    title="Rangmanch Reviews API",
    description="A REST API for managing theatre play reviews.",
    lifespan=lifespan,
)
app.include_router(reviews_router)


@app.get("/")
def root():
    """Return a simple welcome response and confirm the API is running."""
    return {"message": "Welcome to the Rangmanch Reviews API!"}     