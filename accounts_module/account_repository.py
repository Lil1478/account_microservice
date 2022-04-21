from models.account_model import User


class AccountRepository:
    def __init__(self, account_dao):
        self.account_dao = account_dao
        print("AccountRepository")

    def add_user(self, user: User):
        return self.account_dao.add_user(user)
        # return "user added"

    def get_users(self):
        return self.account_dao.get_all()
        # return "user getted"

    def get_user_by_id(self, user_id):
        return self.account_dao.get_user(user_id)
        # return "user getted by id"

    def delete_user(self, user_id):
        return self.account_dao.delete_user(user_id)
        # return "user deleted"
