from fastapi import FastAPI

from app.api.routes import conversations, messages, users

app = FastAPI(title="Parenting App API")

# Include routers
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(conversations.router, prefix="/api/v1", tags=["conversations"])
app.include_router(messages.router, prefix="/api/v1", tags=["messages"])

@app.get("/")
async def root():
    return {"message": "Parenting App API"}
