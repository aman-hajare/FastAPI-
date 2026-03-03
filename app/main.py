from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine) ## no need here for create table cause we use alembic for create table

app = FastAPI()

# origins = ["https://www.google.com", "https://www.youtube.com"]

origins = ["*"] 
###fetch('http://localhost:8000/').then(res => res.json()).then(console.log) ## for check on any website use this
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/") # if both path are same ("/") fastapi choose first one ex.here root()
async def root():
    return {"message": "Hello World"}



"""
In Pydantic v2:

.dict() → ❌ deprecated

.json() → ❌ deprecated

.class Config: 
        from_attributes = True → ❌ deprecated

.model_dump() → ✅ correct

.model_dump_json() → ✅ correct

.model_config = ConfigDict(from_attributes=True) → ✅ correct

"""
