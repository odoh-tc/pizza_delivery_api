from fastapi import FastAPI, status
from routers.auth import auth_router
# from routers.order import order_router
from routers.user import user_router
from routers.order import order_router
from routers.staff import staff_router
from logger import logger
from database import engine
import models


app = FastAPI()


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(order_router)
app.include_router(staff_router)

logger.info("starting app")

models.Base.metadata.create_all(bind=engine)


@app.get("/", status_code=status.HTTP_200_OK)
async def home():
    return {"message": "Welcome to our home page!"}
                                                   