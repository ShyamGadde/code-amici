import json
import sys

sys.path.append("/app")

from app.database import SessionLocal
from app.models import User

session = SessionLocal()

with open(sys.argv[1]) as file:
    for user in json.load(file):
        user_db = User(**user)
        session.add(user_db)
        session.commit()
