from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.todo import TodoCreate, TodoResponse
from app.core.database import get_db
from app.crud.todos import create_todo, get_todos, get_todo, update_todo, delete_todo

router = APIRouter(prefix="/todos", tags=["todos"])

@router.post("/", response_model=TodoResponse)
def create_todo_endpoint(todo: TodoCreate, db: Session = Depends(get_db)):
    return create_todo(db, todo)

@router.get("/", response_model=List[TodoResponse])
def read_todos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_todos(db, skip=skip, limit=limit)

@router.get("/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = get_todo(db, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo_endpoint(todo_id: int, todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = update_todo(db, todo_id, todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.delete("/{todo_id}")
def delete_todo_endpoint(todo_id: int, db: Session = Depends(get_db)):
    db_todo = delete_todo(db, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"detail": "Todo deleted"}
