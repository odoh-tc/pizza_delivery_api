from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status
from fastapi import APIRouter, Depends, HTTPException, status
from services.auth import get_hash_password, get_current_user, verify_password, token_generator
from schema.user import LoginModel, SignUpModel
from schema.order import OrderModel
import models
from database import get_db
from logger import logger
from database import engine


db_dependency = Annotated[Session, Depends(get_db)]


order_router = APIRouter(
    prefix="/order",
    tags=["order"],
    responses={404: {"description": "Not found"}},
)

models.Base.metadata.create_all(bind=engine)


@order_router.post("/", status_code=status.HTTP_201_CREATED)
async def place_an_order(db: db_dependency, order: OrderModel, user: LoginModel = Depends(get_current_user)):

    try:
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not authenticated",
            )
        
        new_order = models.Order(
            pizza_size = order.pizza_size,
            quantity = order.quantity,
        )

        new_order.user = user

        db.add(new_order)

        db.commit()

        return {
            "message": "Order placed successfully",
            "order": new_order.serialize()
        }
    
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@order_router.get("/", status_code=status.HTTP_200_OK)
async def get_user_orders(db: db_dependency, user: LoginModel = Depends(get_current_user)):
    try:
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not authenticated",
            )

        orders = db.query(models.Order).filter(models.Order.user_id == user.id).all()

        if orders:
            return {
                "status": "success",
                "orders": [order.serialize() for order in orders]
            }
        else:
            return {
                "status": "success",
                "message": "No orders found."
            }
    
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    

@order_router.get("/{id}/", status_code=status.HTTP_200_OK)
async def get_user_specific_order(db: db_dependency, id: int, user: LoginModel = Depends(get_current_user)):
    try:
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not authenticated",
            )

        order = db.query(models.Order).filter(models.Order.id == id, models.Order.user_id == user.id).first()

        if order:
            return {
                "status": "success",
                "order": order.serialize()
            }
        else:
            return {
                "status": "success",
                "message": "Order not found"
            }
    
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )




@order_router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_order(db: db_dependency, id: int, order_data: OrderModel, user: LoginModel = Depends(get_current_user)):
    try:
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not authenticated",
            )

        db_order = db.query(models.Order).filter(models.Order.id == id, models.Order.user_id == user.id).first()

        if db_order:
            db_order.pizza_size = order_data.pizza_size
            db_order.quantity = order_data.quantity

            db.commit()

            return {
                "status": "success",
                "order": db_order.serialize()
            }
        else:
            return {
                "status": "success",
                "message": "Order not found"
            }
        
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )



@order_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(db: db_dependency, id: int, user: models.User = Depends(get_current_user)):

    try:
        order = db.query(models.Order).filter(models.Order.id == id, models.Order.user_id == user.id).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )

        db.delete(order)
        db.commit()

        return None

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )





























