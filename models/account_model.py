from sqlalchemy import Column, Integer, String

from database import Base


class User(Base):
    __tablename__ = 'Users'
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String(120), nullable=False)
    last_name = Column(String(120), nullable=False)
    email = Column(String(220), nullable=False, unique=True)
    password = Column(String(10), nullable=False)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def to_json(self):
        return {
            'id': self.person_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
        }
