from datetime import timedelta
from urllib import request

from fastapi import Depends, APIRouter, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from accounts_module.account_dao import AccountDAO
from accounts_module.account_repository import AccountRepository, get_current_active_user
from helpers.token_helpers import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from models.token_model import Token
from schemas.account_schemas import User

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

account_dao = AccountDAO()
account_repository = AccountRepository(account_dao)


@router.post("")
def add_user(new_user: User):
    result = account_repository.add_user(new_user)
    if result == "NO_EMAIL":
        raise HTTPException(status_code=400, detail="Incorrect email")
    if result == "USER_EXISTS":
        raise HTTPException(
            status_code=400, detail="User with this username is already exist")
    return result


@router.post("/auth")
def authorizate_user(auth_user: User):
    result = account_repository.authenticate_user(
        auth_user.username, auth_user.password)
    if result == "AUTH_FALSE":
        raise HTTPException(
            status_code=401, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": auth_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("")
async def get_users(current_user: User = Depends(get_current_active_user)):
    return account_repository.get_users()


@router.patch("/password")
async def get_users(request: Request, current_user: User = Depends(get_current_active_user)):
    body = await request.json()
    password = body['password']
    return account_repository.change_password(current_user, password)


@router.get("/current")
async def read_current_user(req: Request, current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/{user_id}")
async def get_user(user_id: int, current_user: User = Depends(get_current_active_user)):
    return account_repository.get_user_by_id(user_id)


@router.put("/{user_id}")
def update_user(user_id: int, new_user: User, current_user: User = Depends(get_current_active_user)):
    result = account_repository.update_user(user_id, new_user, current_user)
    if result == "ACCESS_TOKEN_REQUIRED":
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": new_user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    return result


@router.delete("/{user_id}")
async def delete_user(user_id: int, current_user: User = Depends(get_current_active_user)):
    return account_repository.delete_user(user_id)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = account_repository.authenticate_user(
        form_data.username, form_data.password)
    if user == "AUTH_FALSE":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
