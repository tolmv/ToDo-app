from pydantic import BaseModel

class TodoBase(BaseModel):
    title: str
    description: str = None

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class TodoPermission(BaseModel):
    user_id: int
    can_read: bool = False
    can_update: bool = False