from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from auth.action import get_current_user
from crud.user import UserCRUD
from crud.dependencies import get_user_crud
from schemas import user as user_schema

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[user_schema.UserResponse])
async def get_users(db: UserCRUD = Depends(get_user_crud)):
    return await db.get_users()


@router.post("", response_model=user_schema.UserResponse)
async def register(
    new_user: user_schema.UserRegister, db: UserCRUD = Depends(get_user_crud)
):
    db_user = await db.get_user_by_email(email=new_user.email)
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    created_user = await db.create_user(new_user)
    return created_user


@router.delete("", deprecated=True)
async def delete_user(
    current_user: user_schema.UserResponse = Depends(get_current_user),
    db: UserCRUD = Depends(get_user_crud),
):
    # return await db.delete_user(email=current_user.email)
    return "deprecated"


@router.put("/password", deprecated=True)
async def update_password(
    request: user_schema.PasswordUpdate,
    current_user: user_schema.UserResponse = Depends(get_current_user),
    db: UserCRUD = Depends(get_user_crud),
):
    # return await db.update_password(email=current_user.email, password=request.password)
    return "deprecated"


@router.put("/profile", deprecated=True)
async def update_profile(
    request: user_schema.UserUpdate,
    current_user: user_schema.UserResponse = Depends(get_current_user),
    db: UserCRUD = Depends(get_user_crud),
):
    # return await db.update_user(email=current_user.email, user_update=request)
    return "deprecated"


@router.get("/me", response_model=user_schema.UserResponse, deprecated=True)
async def protected(current_user: user_schema.UserResponse = Depends(get_current_user)):
    # return current_user
    return "deprecated"
