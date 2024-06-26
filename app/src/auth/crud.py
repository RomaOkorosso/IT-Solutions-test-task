from datetime import datetime

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from logger import logger
from app.src.auth.models import User, Token
from app.src.auth.schemas import UserCreate, UserUpdate, TokenCreate, TokenUpdate
from app.src.base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_user_by_username(self, session: AsyncSession, username: str):
        """
        return User model by username
        :param session: AsyncSession
        :param username: str
        :return: model.User
        """
        logger.log(f"{datetime.now()} - get user by username: {username}")
        db_user = (
            await session.execute(
                select(self.model).where(self.model.username == username)
            )
        ).scalar_one_or_none()
        logger.log(f"{datetime.now()} - User: {db_user}")
        return db_user

    async def get_by_token(self, session: AsyncSession, token: Token):
        """
        return User by Token
        :param session:
        :param token:
        :return: user
        """

        logger.log(f"{datetime.now()} - get user by token {token}")
        db_user = (
            await session.execute(
                select(self.model).where(self.model.id == token.user_id)
            )
        ).scalar_one_or_none()
        return db_user

    async def get_by_access_token(self, session: AsyncSession, token: str):
        """
        return User by Token
        :param session:
        :param token:
        :return: user
        """
        logger.log(f"token - {token}")
        token = await crud_token.get_by_access_token(
            session=session, access_token=token
        )

        logger.log(f"{datetime.now()} - get user by token {token}")
        db_user = (
            await session.execute(
                select(self.model).where(self.model.id == token.user_id)
            )
        ).scalar_one_or_none()
        return db_user


crud_user = CRUDUser(User)


class CRUDToken(CRUDBase[Token, TokenCreate, TokenUpdate]):
    async def get_by_access_token(self, session: AsyncSession, access_token: str):
        """
        return token by str
        :param session: AsyncSession
        :param access_token: str
        :return: models.Token
        """
        logger.log(f"{datetime.now()} - get token by access token: {access_token}")
        return (
            await session.execute(
                select(self.model).where(self.model.token == access_token)
            )
        ).scalar_one_or_none()

    async def revoke(self, session: AsyncSession, token: str) -> None:
        """
        recreate access token
        :param session: AsyncSession
        :param token: str
        :return: None
        """
        logger.log(f"{datetime.now()} - revoke token: {token}")
        query = delete(self.model).where(self.model.token == token)
        await session.execute(query)
        await session.commit()
        return

    async def create_or_pass(self, session: AsyncSession, *, obj_in: Token) -> Token:
        """

        :param session:
        :param obj_in:
        :return:
        """
        logger.log(f"{datetime.now()} - create or pass token")

        old_token = (
            await session.execute(
                select(self.model)
                .where(self.model.user_id == obj_in.user_id)
                .where(self.model.expire_at > datetime.utcnow())
                .order_by(self.model.expire_at)
                .limit(1)
            )
        ).scalar_one_or_none()

        if not old_token:
            return await self.create(db=session, obj_in=obj_in)
        else:
            logger.log(f"{datetime.now()} - old_token - {old_token.__dict__}")

        return old_token


crud_token = CRUDToken(Token)
