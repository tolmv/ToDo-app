from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.database import get_db
from app.models.todo import Todo, UserTodoPermission
from app.models.user import User
from app.schemas.todo import TodoCreate, Todo as TodoSchema, TodoPermission

router = APIRouter()

@router.post("/todos", response_model=TodoSchema)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_todo = Todo(**todo.dict(), owner_id=current_user.id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.get("/todos/{todo_id}", response_model=TodoSchema)
def read_todo(todo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo.owner_id != current_user.id:
        permission = db.query(UserTodoPermission).filter(UserTodoPermission.user_id == current_user.id, UserTodoPermission.todo_id == todo_id).first()
        if not permission or not permission.can_read:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    return todo

@router.put("/todos/{todo_id}", response_model=TodoSchema)
def update_todo(todo_id: int, todo: TodoCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if db_todo.owner_id != current_user.id:
        permission = db.query(UserTodoPermission).filter(UserTodoPermission.user_id == current_user.id, UserTodoPermission.todo_id == todo_id).first()
        if not permission or not permission.can_update:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    for key, value in todo.dict().items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.delete("/todos/{todo_id}", response_model=TodoSchema)
def delete_todo(todo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db.delete(todo)
    db.commit()
    return todo

@router.post("/todos/{todo_id}/permissions")
def set_todo_permissions(todo_id: int, permission: TodoPermission, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo or todo.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db_permission = db.query(UserTodoPermission).filter(UserTodoPermission.user_id == permission.user_id, UserTodoPermission.todo_id == todo_id).first()
    if db_permission:
        db_permission.can_read = permission.can_read
        db_permission.can_update = permission.can_update
    else:
        db_permission = UserTodoPermission(user_id=permission.user_id, todo_id=todo_id, can_read=permission.can_read, can_update=permission.can_update)
        db.add(db_permission)
    db.commit()
    return {"status": "success"}