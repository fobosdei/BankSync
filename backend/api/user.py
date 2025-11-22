from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from auth.action import get_current_user
from crud.dependencies import get_user_crud
from crud.user import UserCRUD
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


@router.put("/{user_id}", response_model=user_schema.UserResponse)
async def update_user(
    user_id: UUID,
    request: user_schema.UserUpdate,
    db: UserCRUD = Depends(get_user_crud),
    current_user: user_schema.UserResponse = Depends(get_current_user),
):
    """
    Actualizar datos básicos de un usuario (full_name, role).
    No se tocan contraseñas ni se borra nada.
    """
    target = await db.get_user_by_id(user_id=user_id)
    if not target:
        raise HTTPException(status_code=404, detail="User not found")

    await db.update_user_by_id(user_id=user_id, user_update=request)
    updated = await db.get_user_by_id(user_id=user_id)
    return updated


@router.post("/{user_id}/deactivate", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_user(
    user_id: UUID,
    db: UserCRUD = Depends(get_user_crud),
    current_user: user_schema.UserResponse = Depends(get_current_user),
):
    """
    Desactivar un usuario marcando su rol como 'inactive' (no elimina datos).
    """
    target = await db.get_user_by_id(user_id=user_id)
    if not target:
        raise HTTPException(status_code=404, detail="User not found")

    await db.deactivate_user_by_id(user_id=user_id)
    return None
