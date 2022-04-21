from database import Base, engine
from models.account_model import User

print("Create database...")
Base.metadata.create_all(engine)