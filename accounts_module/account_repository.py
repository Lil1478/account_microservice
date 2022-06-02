import re

from accounts_module.account_dao import AccountDAO
from helpers.token_helpers import ALGORITHM, SECRET_KEY
from models.account_model import User
from passlib.context import CryptContext

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from models.token_model import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
account_dao = AccountDAO()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def check_len_password(password):
    return len(password)>=6

def validate_email(username):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", username):
        # raise AssertionError('Provided email is not an email address')
        return "NO_EMAIL"
    return username


class AccountRepository:
    def __init__(self, account_dao):
        self.account_dao = account_dao
        print("AccountRepository")

    def authenticate_user(self, username: str, password: str):
        user = self.get_user_by_email(username)
        if not user:
            return "AUTH_FALSE"
        if not verify_password(password, user.password):
            return "AUTH_FALSE"
        return user

    def add_user(self, user: User):
        validation_email_result = validate_email(user.username)
        if validation_email_result == "NO_EMAIL":
            return "NO_EMAIL"
        user_db = self.account_dao.get_user_by_email(user.username)
        if user_db is not None:
            return "USER_EXISTS"
        if not check_len_password(user.password):
            return "PASSWORD_TOO_SHORT"
        hash_password = get_password_hash(user.password)
        user.password = hash_password
        return self.account_dao.add_user(user)

    def get_users(self):
        return self.account_dao.get_all()

    def change_password(self, current_user: User, password):
        if not check_len_password(password):
            return "PASSWORD_TOO_SHORT"
        hash_password = get_password_hash(password)
        return self.account_dao.change_password(current_user.user_id, hash_password)

    def update_user(self, user_id, new_user: User, current_user: User):
        db_user = self.account_dao.get_user(user_id)
        if db_user is None:
            return "NO_USER"
        result = self.account_dao.update_user(user_id, new_user)
        if current_user.user_id == db_user.user_id:
            return "ACCESS_TOKEN_REQUIRED"
        return result

    def get_user_by_id(self, user_id):
        return self.account_dao.get_user(user_id)

    def get_user_by_email(self, username):
        return self.account_dao.get_user_by_email(username)

    def delete_user(self, user_id):
        return self.account_dao.delete_user(user_id)


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = account_dao.get_user_by_email(token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user
