import os

class Config:
    ENV = os.getenv("ENV", "development")
    DEBUG = (ENV != "production")
    
    # Define default CORS origins
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000"  # React dev server in local development
    ] if DEBUG else [
        "https://four-of-gang-frontend.vercel.app"  # Deployed frontend URL
    ]

