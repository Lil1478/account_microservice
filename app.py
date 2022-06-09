import os

import uvicorn
from fastapi import FastAPI
from accounts_module import account_controller, google_auth
from database import SessionLocal, Base, engine
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.include_router(account_controller.router)
app.include_router(google_auth.router_google)

app.add_middleware(SessionMiddleware, secret_key="example")

db = SessionLocal()

if __name__ == '__main__':
    # init_account_module()
    # server_port = os.environ.get('PORT', '8080')
    uvicorn.run(app, port='8080', host='0.0.0.0')