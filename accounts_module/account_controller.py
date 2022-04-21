from fastapi import APIRouter
from accounts_module.account_dao import AccountDAO
from accounts_module.account_repository import AccountRepository
from schemas.account_schemas import User

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

# class AccountControllers:
#     def __init__(self, repository):
#         self.repository = repository
#         print('AccountControllers')

account_dao = AccountDAO()
account_repository = AccountRepository(account_dao)


@router.post("/")
def add_user(new_user: User):
    result = account_repository.add_user(new_user)
    return result


@router.get("/")
async def get_users():
    return account_repository.get_users()


@router.get("/{user_id}")
async def get_user(user_id: int):
    return {'id': 1,
            'first_name': "first name",
            'last_name': "second name",
            'email': "email",
            'password': "password"}
    # return account_repository.get_user_by_id(user_id)


@router.put("/{user_id}")
def update_user(user_id: int, new_user: User):
    return {"user_name": new_user.name, "user_id": user_id}


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    return account_repository.delete_user(user_id)
