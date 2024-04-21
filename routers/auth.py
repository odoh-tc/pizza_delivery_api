from datetime import timedelta
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from services.auth import token_generator, authenticate_user, get_db


db_dependency = Annotated[Session, Depends(get_db)]


auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@auth_router.post('/token', status_code=status.HTTP_201_CREATED)
async def generate_token(db: db_dependency, request_form: OAuth2PasswordRequestForm = Depends()):
    token = await token_generator(db, request_form.username, request_form.password)
    return {
        'access_token': token,
        'token_type': 'bearer',
    }


