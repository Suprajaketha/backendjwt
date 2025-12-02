from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.api.routes import router

# -----------------------
# CREATE APP FIRST
# -----------------------
app = FastAPI(
    title="FastAPI JWT Role Based API",
    version="1.0.0"
)

# -----------------------
# ADD CUSTOM OPENAPI AFTER APP IS CREATED
# -----------------------
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="FastAPI JWT Role Based API",
        version="1.0.0",
        description="JWT Authentication & Role Based Access",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# -----------------------
# CORS
# -----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# ROUTES
# -----------------------
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Backend running!"}
