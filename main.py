from fastapi import FastAPI
from database import init_db
from api.routes import router as reviewRouter

app = FastAPI()

app.include_router(reviewRouter)

@app.on_event('startup')
def startup():
    init_db()