import uvicorn
from fastapi import FastAPI
from accounts_module import account_controller
# from database import SessionLocal

app = FastAPI()
app.include_router(account_controller.router)

# db = SessionLocal()

if __name__ == '__main__':
    # init_account_module()
    uvicorn.run(app)
