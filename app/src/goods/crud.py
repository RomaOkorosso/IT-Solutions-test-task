import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.base import CRUDBase
from app.src.goods.models import Good
from app.src.goods.schemas import GoodCreate, GoodUpdate
from logger import logger


class CRUDGood(CRUDBase[Good, GoodCreate, GoodUpdate]):
    async def get_by_headline(self, session: AsyncSession, headline: str) -> Good or None:
        """
        get one of ad/good by article/headline

        :param session: AsyncSession
        :param headline: str (article of ad/good)
        :return: Good or None
        """
        logger.log(f"{datetime.datetime.now()} - get good by headline ({headline})")
        try:
            db_good = (
                await session.execute(
                    select(self.model).where(self.model.headline == headline)
                )
            ).scalar_one_or_none()
        except Exception as err:
            logger.log(f"{datetime.datetime.now()} - err while get good by headline - {err}")
            return None  # TODO rewrite to normal behavior (raise err)
        return db_good

    async def create_or_pass(self, session: AsyncSession, *, obj_in: GoodCreate):
        """
        create or pass creation of good
        :param session: AsyncSession
        :param obj_in: models.Good
        :return: models.Good
        """
        logger.log(f"{datetime.datetime.now()} - try to create or pass {obj_in}")
        db_good = await crud_good.get_by_headline(session=session, headline=obj_in.headline)
        if db_good is None:
            try:
                db_good = await crud_good.create(db=session, obj_in=obj_in)
            except Exception as err:
                logger.log(f"{datetime.datetime.now()} - err while create good - {err}")
        logger.log(f"{datetime.datetime.now()} - created or use existing good ")
        return db_good


crud_good = CRUDGood(Good)
