import re
from sqlalchemy.orm import validates
from fastapi import status, HTTPException

# from database import SessionLocal
from models.account_model import User

# db = SessionLocal()


@validates('email')
def validate_email(email):
    users = User.query.all()
    for user in users:
        if user.to_json()['email'] == str(email):
            raise AttributeError('Used email')
    if not email:
        raise AttributeError('No email provided')
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise AssertionError('Provided email is not an email address')
    return email


class AccountDAO:
    def __init__(self, ):
        self.collection_name = "Users"

    def get_all(self):
        users = db.query(User).all()
        return users

    def add_user(self, user: User):
        user = User(user.first_name, user.last_name, user.email, user.password)
        db.add(user)
        db.commit()
        return self.get_user_by_email(user.email)

    def get_user(self, user_id):
        user_db = db.query(User).filter(User.user_id == user_id).first()
        return user_db

    def get_user_by_email(self, email):
        user_db = db.query(User).filter(User.email == email).first()
        return user_db

    def delete_user(self, user_id):
        user_db = db.query(User).filter(User.user_id == user_id).first()
        if user_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource Not Found")
        db.delete(user_db)
        db.commit()
        return "SUCCESS"
