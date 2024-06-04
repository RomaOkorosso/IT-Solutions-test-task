from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from logger import logger
from app.src.goods import crud, schemas, service
from app.src.auth import schemas as auth_schemas, routes as auth_routes
from app.src.base import get_session

router = APIRouter(prefix="/goods", tags=["goods"])


@router.get("/all")
async def get_all_goods(
    session: AsyncSession = Depends(get_session),
    _: auth_schemas.UserInDB = Depends(auth_routes.get_authed_user),
):
    try:
        goods = await crud.crud_good.get_all(db=session)
    except Exception as err:
        logger.log(f"{datetime.now()} - get all goods err: {err}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Unexpected error")
    return goods


@router.get("/{good_id}")
async def get_by_id(
    good_id: int,
    session: AsyncSession = Depends(get_session),
    _: auth_schemas.UserInDB = Depends(auth_routes.get_authed_user),
):
    try:
        good_in_db = await crud.crud_good.get(db=session, id=good_id)
    except Exception as err:
        logger.log(f"{datetime.now()} - get all good {good_id} err: {err}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "")
    if good_in_db is not None:
        return good_in_db
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Item not found")


@router.put("/{good_id}")
async def update_good_by_id(
    good_id: int,
    good_update: schemas.GoodUpdate,
    session: AsyncSession = Depends(get_session),
    _: auth_schemas.UserInDB = Depends(auth_routes.get_authed_user),
):
    """Update any good's fields"""
    try:
        new_db_good = await service.good_service.update_data(
            session, good_id, new_good=good_update
        )
    except Exception as err:
        logger.log(f"{datetime.now()} - err while update good - {err}")
        if isinstance(err, HTTPException):
            raise err
        else:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, err)
    return new_db_good


@router.delete("/{good_id")
async def delete_good(
    good_id: int,
    session: AsyncSession = Depends(get_session),
    _: auth_schemas.UserInDB = Depends(auth_routes.get_authed_user),
):
    """
    delete good by id
    """
    try:
        db_good = await crud.crud_good.get(db=session, id=good_id)
    except Exception as err:
        logger.log(f"{datetime.now()} - err while getting good from db - {err}")
        if isinstance(err, HTTPException):
            raise err
        else:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Undefined error")
    if db_good is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Item not found")
    else:
        try:
            deleted_good = await crud.crud_good.remove(db=session, id=good_id)
        except Exception as err:
            logger.log(f"{datetime.now()} - error while deleting good - {err}")
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Undefiled error")
        return {"deleted_item": deleted_good, "status": True}
