from pydantic import BaseModel

class TodoBase(BaseModel):
    title: str
    description: str

class TodoCreate(TodoBase):
    pass

class TodoResponse(TodoBase):
    id: int
    completed: bool

    class Config:
        orm_mode = True
