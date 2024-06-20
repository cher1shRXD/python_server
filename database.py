from sqlalchemy import create_engine, MetaData
from databases import Database

DATABASE_URL = "mysql+mysqlconnector://root:Tw080401!!**@localhost/python_project"

database = Database(DATABASE_URL)
metadata = MetaData()

engine = create_engine(DATABASE_URL)
