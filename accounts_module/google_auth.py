from datetime import timedelta
import json
from fastapi import APIRouter, FastAPI
from starlette.config import Config
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from accounts_module.account_dao import AccountDAO
from accounts_module.account_repository import get_password_hash

from helpers.token_helpers import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from models.account_model import User


router_google = APIRouter(
    tags=["users_google"]
)

account_dao = AccountDAO()

config = Config('.env')
oauth = OAuth(config)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@router_google.get('/')
async def homepage(request: Request):
    user = request.session.get('user')
    if user:
        data = json.dumps(user)
        html = (
            f'<pre>{data}</pre>'
            '<a href="/logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/login">login</a>')


@router_google.get('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router_google.get('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        print("TOKEEEEN ", token)
    except OAuthError as error:
        print("error ", error)
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user = token.get('userinfo')

    if user:
        print("USERRR ", user)
        request.session['user'] = dict(user)

        username = user['email']
        first_name = user['given_name']
        last_name = user['family_name']
        password = get_password_hash(user['email'])

        user_db = account_dao.add_user(User(first_name, last_name, username, password))

        print("USERRR!!!!!! ", username)  
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router_google.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')
