from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router as api_router

app = FastAPI(
    title="XAU/USD Power Analysis App",
    description="Safety-first decision support system for Gold trading.",
    version="1.0.0"
)

# CORS Middleware (Allow Frontend Access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routes
app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {"status": "active", "system": "XAU/USD Safety Engine"}
