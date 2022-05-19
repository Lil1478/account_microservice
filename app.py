import os

import uvicorn
from fastapi import FastAPI
from accounts_module import account_controller
from database import SessionLocal, Base, engine

app = FastAPI()
app.include_router(account_controller.router)

db = SessionLocal()

if __name__ == '__main__':
    # init_account_module()
    # server_port = os.environ.get('PORT', '8080')
    uvicorn.run(app, port='8080', host='0.0.0.0')