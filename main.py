from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.db.session import engine
from src.models.base import Base
from src.api.endpoints import graph_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)  
            await conn.run_sync(Base.metadata.create_all)
            print("✅ Tables created successfully")
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
        raise

    yield 

    print("🛑 Shutting down...")

app = FastAPI(lifespan=lifespan)

app.include_router(graph_router().router, prefix="/api/graph")

@app.get("/health")
async def health_check():
    return {"status": "ok"}


if __name__ == '__main__':
    import uvicorn, os
    uvicorn.run("main:app", host=os.getenv('HOST'), 
                port=int(os.getenv('PORT')), 
                reload=bool(os.getenv('RELOAD_STRATEGY')))