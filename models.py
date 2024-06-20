from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey
from database import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(50)),
    Column("hashed_password", String(128)),
)

todo = Table(
    "todo",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("author_id", Integer, ForeignKey("users.id")),
    Column("title", String(50)),
    Column("content", String),
    Column("completed", Boolean, default=False),
)
