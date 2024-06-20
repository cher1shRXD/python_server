from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from sqlalchemy import select
from passlib.context import CryptContext

from database import database, engine, metadata
from models import users, todo

metadata.create_all(engine)

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserIn(BaseModel):
    name: str
    password: str


class UserOut(BaseModel):
    id: int
    name: str


class TodoIn(BaseModel):
    author_id: int
    title: str
    content: str
    completed: int = 0


class TodoOut(BaseModel):
    id: int
    author_id: int
    title: str
    content: str
    completed: bool


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(name: str, password: str):
    query = select(users.c.id, users.c.name, users.c.hashed_password).where(users.c.name == name)
    user = await database.fetch_one(query)
    if user:
        stored_hashed_password = user["hashed_password"]
        if pwd_context.verify(password, stored_hashed_password):
            return user
    return None


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/signup/", response_model=UserOut)
async def create_user(user: UserIn):
    hashed_password = get_password_hash(user.password)
    query = users.insert().values(name=user.name, hashed_password=hashed_password)
    last_record_id = await database.execute(query)
    return {"id": last_record_id, "name": user.name}


@app.get("/users/{user_id}", response_model=UserOut)
async def read_user(user_id: int):
    query = select(users.c.id, users.c.name).where(users.c.id == user_id)
    user = await database.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user["id"], "name": user["name"]}


@app.post("/login/")
async def login(user: UserIn):
    user_db = await authenticate_user(user.name, user.password)
    if not user_db:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"user_id": user_db["id"], "name": user_db["name"]}


@app.get('/getTodo/{user_id}', response_model=List[TodoOut])
async def get_todos(user_id: int):
    query = select(todo.c.id, todo.c.author_id, todo.c.title, todo.c.content, todo.c.completed).where(todo.c.author_id == user_id)
    todos = await database.fetch_all(query)
    if not todos:
        raise HTTPException(status_code=404, detail="해당 사용자의 할 일이 없습니다")
    return todos

@app.post('/write')
async def write_todo(todo_content:TodoIn):
    query = todo.insert().values(author_id=todo_content.author_id, title=todo_content.title, content=todo_content.content, completed=todo_content.completed)
    write = await database.execute(query)
    if not write:
        raise HTTPException(status_code=400, detail='알 수 없는 에러')
    return None


@app.patch('/updateState/{todo_id}')
async def update_todo(todo_id: int):
    query = todo.update().where(todo.c.id == todo_id).values(completed=1)
    patch = await database.execute(query)
    if not patch:
        raise HTTPException(status_code=400, detail='알 수 없는 에러')
    return None

# /deleteArtcle - DELETE
# /articles - DELETE

# /articles - PATCH
# /articles - POST (CREATE)
# /articles/{article_id} - GET
# /articles - GET (get all or page)


@app.delete('/deleteTodo/{todo_id}')
async def delete_todo(todo_id: int):
    query = todo.delete().where(todo.c.id == todo_id)
    patch = await database.execute(query)
    if not patch:
        raise HTTPException(status_code=400, detail='알 수 없는 에러')
    return None

