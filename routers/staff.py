from typing import Annotated
from fastapi import APIRouter, HTTPException, status
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from services.auth import get_hash_password, get_current_user, verify_password, token_generator
from schema.user import LoginModel, SignUpModel
from schema.order import OrderModel, OrderStatus
import models
from database import get_db
from logger import logger
from database import engine



db_dependency = Annotated[Session, Depends(get_db)]


staff_router = APIRouter(
    prefix="/staff",
    tags=["staff"],
    responses={404: {"description": "Not found"}},
)

models.Base.metadata.create_all(bind=engine)


@staff_router.get('/', status_code=status.HTTP_200_OK)
async def list_all_orders(db: db_dependency, user: models.User = Depends(get_current_user)):

    try:
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not authenticated",
            )
        
        if user.is_staff:
            orders = db.query(models.Order).all()

            if orders:
                return {
                    "status": "success",
                    "orders": [order.serialize() for order in orders]
                }
            else:
                return {"status": "success", 
                        "message": "No orders found."}
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden. User is not a staff member.",
            )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        )

@staff_router.get('/{id}', status_code=status.HTTP_200_OK)
async def get_order(db: db_dependency, id: int, user: models.User = Depends(get_current_user)):

    try:

        if user.is_staff:
            try:
                order = db.query(models.Order).filter(models.Order.id == id).first()

                if order:
                    return {
                        "status": "success",
                        "order": order.serialize()
                    }
                else:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Order not found.",
                    )
            except Exception as e:
                logger.error(e)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Internal server error.",
                )
            

        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden. User is not a staff member.",
            )
        
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        )
            


@staff_router.put("/{id}", status_code=status.HTTP_201_CREATED)
async def update_order_status(db: db_dependency, id: int, order_status: OrderStatus, 
                              user: models.User = Depends(get_current_user)):

    try:
        if not user.is_staff:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User is not authorized to perform this action",
            )

        if order_status not in OrderStatus:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid order status",
            )

        order = db.query(models.Order).filter(models.Order.id == id).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )

        order.order_status = order_status
        db.commit()

        return {
            "status": "success",
            "order_id": order.id,
            "new_status": order_status,
        }

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )





@staff_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_any_order(db: db_dependency, id: int, user: models.User = Depends(get_current_user)):

    try:
        if not user.is_staff:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User is not authorized to perform this action",
            )

        order = db.query(models.Order).filter(models.Order.id == id).first()
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
