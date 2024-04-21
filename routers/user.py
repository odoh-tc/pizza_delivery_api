from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from services.auth import get_hash_password, get_current_user, verify_password, token_generator
from schema.user import LoginModel, SignUpModel, UpdateUserModel
import models
from database import get_db
from logger import logger
from database import engine


user_router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)

models.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]


@user_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(db: db_dependency, user: SignUpModel):

    """
    ## Signs up a new user.

    Parameters:
    - user (SignUpModel): A model instance containing the user's email, username, password, first_name, and last_name.

    Returns:
    - dict: A dictionary containing a message and the newly created user's serialized data.

    Raises:
    - HTTPException: If the user with the provided email or username already exists.
    """
    
    
    try:
        db_user = db.query(models.User).filter(models.User.email == user.email).first()

        if db_user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with email {user.email} already exists",
            )
        
        db_username = db.query(models.User).filter(models.User.username == user.username).first()

        if db_username is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with username {user.username} already exists",
            )
        
        user_info = user.model_dump()
        user_info["password"] = get_hash_password(user.password)
        new_user = models.User(**user_info)

        db.add(new_user)

        db.commit()


        return {
            "message": "User created successfully",
            "user": new_user.serialize()
        }
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    


@user_router.post("/login", status_code=status.HTTP_200_OK)
async def login(db: db_dependency, user: LoginModel):

    """
    ## Logs in a user.

    Parameters:
    - user (LoginModel): A model instance containing the user's username and password.

    Returns:
    - dict: A dictionary containing the logged-in user's serialized data and a token.

    Raises:
    - HTTPException: If the user with the provided username does not exist or if the password is incorrect.
    """
    try:
        # Query the user from the database based on the provided username
        db_user = db.query(models.User).filter(models.User.username == user.username).first()

        # Check if the user exists and the password is correct
        if db_user is None or not verify_password(user.password, db_user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = await token_generator(db, user.username, user.password)

        # Return user details along with the token
        return {
            "status": "success",
            "user": db_user.serialize(),
            "token": token
        }
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@user_router.get("/me", status_code=status.HTTP_200_OK)
async def get_user_details(db: db_dependency, user: models.User = Depends(get_current_user)):
    

    """
    ## Retrieves the details of the authenticated user.

    Parameters:
    - user (models.User): A model instance containing the user's data.

    Returns:
    - dict: A dictionary containing the user's serialized data and their orders (if any).

    Raises:
    - HTTPException: If the user is not authenticated.
    """
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
                "user": user.serialize(),
                "orders": [order.serialize() for order in orders]
            }
        else:
            return {
                "status": "success",
                "user": user.serialize()
            }

        
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )




@user_router.put("/", status_code=status.HTTP_200_OK)
async def update_user(db: db_dependency, user_details: UpdateUserModel, user: models.User = Depends(get_current_user)):


    """
    ## Updates the details of the authenticated user.

    Parameters:
    - user_details (UpdateUserModel): A model instance containing the updated user's data.
    - user (models.User): A model instance containing the user's data.

    Returns:
    - dict: A dictionary containing the updated user's serialized data.

    Raises:
    - HTTPException: If the user is not authenticated or if the user does not exist.
    """
    try:
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not authenticated",
            )
        

        db_user = db.query(models.User).filter(models.User.id == user.id).first()

        if db_user:

            db_user.username = user_details.username
            db_user.email = user_details.email
            db_user.first_name = user_details.first_name
            db_user.last_name = user_details.last_name

            db.commit()

            return {
                "status": "success",
                "user": db_user.serialize()
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
























