"""Todo items router with CRUD operations."""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel

router = APIRouter()


class TodoCreate(BaseModel):
    """Schema for creating a new todo."""
    title: str
    description: Optional[str] = None
    completed: bool = False


class TodoUpdate(BaseModel):
    """Schema for updating an existing todo."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TodoResponse(BaseModel):
    """Schema for todo response."""
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    user_id: str
    
    class Config:
        from_attributes = True


# In-memory storage for demonstration
# In production, this would be backed by a database
_todos_db = {}
_todo_counter = 1


def get_current_user() -> str:
    """Mock user authentication. In production, verify JWT token."""
    return "user_123"


@router.get("", response_model=List[TodoResponse])
async def list_todos(
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    user_id: str = Depends(get_current_user),
):
    """List all todos for the current user."""
    user_todos = [
        todo for todo in _todos_db.values()
        if todo["user_id"] == user_id
    ]
    
    if completed is not None:
        user_todos = [t for t in user_todos if t["completed"] == completed]
    
    return user_todos


@router.post("", response_model=TodoResponse, status_code=201)
async def create_todo(
    todo: TodoCreate,
    user_id: str = Depends(get_current_user),
):
    """Create a new todo item."""
    global _todo_counter
    
    new_todo = {
        "id": _todo_counter,
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed,
        "user_id": user_id,
    }
    
    _todos_db[_todo_counter] = new_todo
    _todo_counter += 1
    
    return new_todo


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: int,
    user_id: str = Depends(get_current_user),
):
    """Get a specific todo by ID."""
    todo = _todos_db.get(todo_id)
    
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if todo["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return todo


@router.patch("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    user_id: str = Depends(get_current_user),
):
    """Update a todo item (partial update)."""
    todo = _todos_db.get(todo_id)
    
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if todo["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Apply partial updates
    update_data = todo_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        todo[key] = value
    
    return todo


@router.delete("/{todo_id}", status_code=204)
async def delete_todo(
    todo_id: int,
    user_id: str = Depends(get_current_user),
):
    """Delete a todo item."""
    todo = _todos_db.get(todo_id)
    
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if todo["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    del _todos_db[todo_id]
    return None
