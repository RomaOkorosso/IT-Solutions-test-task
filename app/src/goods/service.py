import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.src.base.db.session import get_session_
from app.src.goods import crud, models, schemas
from logger import logger
from app.src.goods.constants import GOODS


class GoodService:
    @staticmethod
    async def feed_data_in_db():
        session: AsyncSession = await get_session_()
        for good in GOODS:
            try:
                good_to_db = schemas.GoodCreate(**good)
            except Exception as err:
                logger.log(
                    f"{datetime.datetime.now()} - an error was accused when parse json to schema. err: {err}"
                )
                raise err
            try:
                await crud.crud_good.create_or_pass(session=session, obj_in=good_to_db)
            except Exception as err:
                logger.log(
                    f"{datetime.datetime.now()} - an error was accused when add schema to db. err: {err}"
                )
                raise err
            logger.log(
                f"{datetime.datetime.now()} - successfully add model {good_to_db.headline} to db"
            )

    @staticmethod
    async def update_data(
        session: AsyncSession, good_id: int, new_good: schemas.GoodUpdate
    ):
        """
        chack is good existed and update fields in db
        :param session: AsyncSession
        :param good_id: int
        :param new_good: schemas.GoodUpdate
        :return: models.Good
        """
        try:
            db_good = await crud.crud_good.get(db=session, id=good_id)
        except Exception as err:
            logger.log(f"{datetime.datetime.now()} - err while get good - {err}")
            raise err
        if db_good is not None:
            try:
                new_db_good = await crud.crud_good.update(
                    db=session, db_obj=db_good, obj_in=new_good
                )
            except Exception as err:
                logger.log(f"{datetime.datetime.now()} - error while update good {err}")
                raise err
            logger.log(
                f"{datetime.datetime.now()} - updated data for good to {new_db_good.__dict__}"
            )
            return new_db_good
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Item not found")


good_service = GoodService()
