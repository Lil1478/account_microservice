import re
from sqlalchemy.orm import validates
from fastapi import status, HTTPException

from database import SessionLocal
from models.account_model import User

db = SessionLocal()


class AccountDAO:
    def __init__(self, ):
        self.collection_name = "users"

    def get_all(self):
        users = db.query(User).all()
        return users

    def add_user(self, user: User):
        user = User(user.first_name, user.last_name, user.username, user.password)
        db.add(user)
        db.commit()
        return self.get_user_by_email(user.username)

    def get_user(self, user_id):
        user_db = db.query(User).filter(User.user_id == user_id).first()
        return user_db

    def get_user_by_email(self, username):
        user_db = db.query(User).filter(User.username == username).first()
        return user_db

    def delete_user(self, user_id):
        user_db = db.query(User).filter(User.user_id == user_id).first()
        if user_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource Not Found")
        db.delete(user_db)
        db.commit()
        return "SUCCESS"

    def update_user(self, user_id, new_user:User):
        db_user = db.query(User).filter(User.user_id == user_id).first()
        db_user.first_name = new_user.first_name
        db_user.last_name = new_user.last_name
        db_user.username = new_user.username
        # db_user.password = new_user.password
        return self.get_user(user_id)
