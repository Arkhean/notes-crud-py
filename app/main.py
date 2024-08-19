import uvicorn
from fastapi import FastAPI

from app.db import Base, engine
from app.router import router

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    # reset db
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # run server
    uvicorn.run(app=app)
