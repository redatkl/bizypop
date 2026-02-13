from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, promo_codes

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Promo Codes API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(promo_codes.router)

@app.get("/")
def root():
    return {"message": "Promo Codes API"}