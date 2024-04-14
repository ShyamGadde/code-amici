import json
import os
import sys

sys.path.append("/app")

from app.core.db import SessionLocal
from app.models import User

session = SessionLocal()

# Get the directory of the current script
utils_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(utils_dir, "users.json")

with open(file_path) as file:
    for user in json.load(file):
        user_db = User(**user)
        session.add(user_db)
        session.commit()
