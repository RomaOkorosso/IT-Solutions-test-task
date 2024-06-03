from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from logger import logger
from app.src.auth import schemas, service, models, crud
from app.src.auth.crud import crud_token
from app.src.auth.models import Token
from app.src.base import get_session, settings
from app.src.base.exceptions import WeakPassword

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_user(
        token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)
) -> schemas.UserInDB:
    logger.log(f"token ={token}")
    return await crud.crud_user.get_by_access_token(session=session, token=token)


async def get_authed_user(user: schemas.UserInDB = Depends(get_user)) -> schemas.UserInDB:
    if not user:
        raise HTTPException(status_code=403, detail="Not authorized")
    return user


@router.post("/register")
async def register(
        full_name: str = Form(...),
        email: str = Form(...),
        username: str = Form(...),
        password: str = Form(...),
        session: AsyncSession = Depends(get_session),
):
    logger.log(f"{datetime.now()} - (auth.routes) Register post")
    try:
        user = schemas.UserCreate(
            full_name=full_name, email=email, username=username, password=password
        )
    except WeakPassword:
        raise HTTPException(400, "weak password")

    password_hash = service.auth_service.get_password_hash(user.password)
    user_dict = user.dict()
    user_dict["password"] = password_hash
    new_user = models.User(**user_dict)
    new_user: models.User = await crud.crud_user.create(db=session, obj_in=new_user)

    access_token = service.auth_service.create_access_token(
        {"username": new_user.username}
    )

    # Save access token in database
    await service.auth_service.create_token(
        session=session, username=new_user.username, access_token=access_token
    )

    logger.log(
        f"{datetime.now()} - (auth.routes) Register post - {new_user.__dict__} - {access_token}"
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login")
async def login_post(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_session),
):
    logger.log(f"{datetime.now()} - (auth.routes) Login post")
    user = await service.auth_service.authenticate_user(
        username=form_data.username, password=form_data.password, session=session
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = service.auth_service.create_access_token(data={"sub": user.username})
    token = Token(token=access_token, user_id=user.id)
    await crud_token.create(session, obj_in=token)

    logger.log(
        f"{datetime.now()} - (auth.routes) Login post - {user.__dict__} - {access_token}"
    )
    logger.log(f"token =={token}")
    return {"access_token": token.token, "token_type": "bearer"}


@router.post("/token")
async def login_by_token(
        token: schemas.TokenBase, session: AsyncSession = Depends(get_session)
) -> schemas.UserInDB:
    try:
        token = await service.crud_token.get_by_access_token(
            session=session, access_token=token.access_token
        )
    except Exception as err:
        logger.log(f"{datetime.now()} - (auth.routes) token post - {token} - {err}")
        raise HTTPException(500, f"some exception was accused {err}")
    if token is not None:
        db_user: schemas.UserInDB = await crud.crud_user.get_by_token(
            session=session, token=token
        )
    else:
        raise HTTPException(400, "Undefined token")
    if db_user is None:
        raise HTTPException(400, "User not found")
    return db_user


@router.delete("/delete_user/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    try:
        await service.crud_user.remove(db=session, id=user_id)
    except Exception as err:
        logger.log(f"{datetime.now()} - (auth.routes) Login post - {user_id} - {err}")
        raise HTTPException(500, f"some exception was accused {err}")
    return {"status": "ok"}
