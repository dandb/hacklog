from sqlalchemy.orm import sessionmaker
from entities import db

Session = sessionmaker(db)
