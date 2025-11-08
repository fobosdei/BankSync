from fastapi import APIRouter, Depends

from auth.action import get_current_user
from crud.user import UserCRUD
from crud.dependencies import get_user_crud
from schemas import user as user_schema

router = APIRouter(prefix="/me", tags=["me"])


@router.delete("")
async def delete_user(
    current_user: user_schema.UserResponse = Depends(get_current_user),
    db: UserCRUD = Depends(get_user_crud),
):
    await db.delete_user(email=current_user.email)
    return {"message": "User deleted successfully"}


@router.put("/password")
async def update_password(
    request: user_schema.PasswordUpdate,
    current_user: user_schema.UserResponse = Depends(get_current_user),
    db: UserCRUD = Depends(get_user_crud),
):
    await db.update_password(email=current_user.email, password=request.password)
    return {"message": "Password updated successfully"}


@router.put("/profile")
async def update_profile(
    request: user_schema.UserUpdate,
    current_user: user_schema.UserResponse = Depends(get_current_user),
    db: UserCRUD = Depends(get_user_crud),
):
    await db.update_user(email=current_user.email, user_update=request)
    return {"message": "Profile updated successfully"}


@router.get("", response_model=user_schema.UserResponse)
async def get_me(current_user: user_schema.UserResponse = Depends(get_current_user)):
    return current_user
