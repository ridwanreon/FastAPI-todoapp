from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel
from typing import Annotated
from datetime import timedelta,datetime,timezone
from sqlalchemy.orm import Session
from models import Users
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from database import SessionLocal
from jose import jwt   
from router.auth import get_current_user
from models import Todos

from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]



@router.get('/admin/todo')
def read_all(user : user_dependency,db : db_dependency):
    
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Failed Authentication')
    
    
    return db.query(Todos).all()


@router.delete('/admin/delete/{todo_id}')
def delete_todos_by_admin(user : user_dependency, db : db_dependency, todo_id : int):
    if user is None or user.get('role' != 'admin'):
        raise HTTPException(status_code=404, detail= 'Authentication Faield')
    
    
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="To do not found")
    
    
    db.delete(todo)
    db.commit()
    return JSONResponse(status_code=200, content={'message' : 'To do deleted successfully'})