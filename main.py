from fastapi import FastAPI,Depends,HTTPException
import models
from database import engine,SessionLocal
from typing import Annotated,Optional
from sqlalchemy.orm import Session
from models import Todos,Users
from pydantic import BaseModel,Field
from fastapi.responses import JSONResponse

from router import auth,admin
from router.auth import get_current_user
app = FastAPI()

models.Base.metadata.create_all(bind = engine)
app.include_router(auth.router)
app.include_router(admin.router)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]


class Todo(BaseModel):
    id : int 
    title : str
    description : str = Field(max_length=100)
    priority : int = Field(gt = 0, lt = 6)
    completed : bool


class TodoUpdate(BaseModel):
    title : Optional[str] = Field(default=None)
    description : Optional[str] = Field(default=None,max_length=100)
    priority : Optional[int] = Field(default=None,gt=0, lt= 6)
    completed : Optional[bool] = Field(default=None)




@app.get('/')
def read_todos(user : user_dependency,db : db_dependency):
    
    if user is None:
        raise HTTPException(status_code=401, detail='Failed Authentication')
    
    
    return db.query(Todos).filter(Todos.owner_id == user.get('user_id')).all()



@app.get('/todo/{todo_id}')
def read_specific_id(user : user_dependency,db : db_dependency,todo_id : int):
    specific_id = db.query(Todos).filter(Todos.owner_id == user.get('user_id')).filter(Todos.id == todo_id).first()
    if specific_id is not None:
        return specific_id
    else:
        raise HTTPException(status_code=404, detail='Todo not found')
    
@app.post('/create/')
def create_todos(user: user_dependency,db : db_dependency, new_todo : Todo):
    
    if user is None:
        raise HTTPException(status_code=401, detail='Failed Authentication')
    
    todo_model = Todos(**new_todo.model_dump(),owner_id = user.get('user_id'))
    db.add(todo_model)
    db.commit() 
    
    return JSONResponse(status_code=201, content= {'message' : 'To do created successfully'})

@app.put('/edit/{todo_id}')
def update_todos(user : user_dependency, db : db_dependency, todo_id : int, update_todo : TodoUpdate):
    todo = db.query(Todos).filter(Todos.owner_id == user.get('user_id')).filter(Todos.id == todo_id).first()
    
    if todo is None:
        raise HTTPException(status_code = 404, detail='To do not found')
    
    update_data = update_todo.model_dump(exclude_unset=True)
    
    for key,value in update_data.items():
        setattr(todo,key,value)
    
    db.commit()
    
    return JSONResponse(status_code=200, content = {'message' : 'To do Succenssfully updated'})


@app.delete('/delete/{todo_id}')
def delete_todo(user : user_dependency,db : db_dependency, todo_id : int):
    todo = db.query(Todos).filter(Todos.owner_id == user.get('user_id')).filter(Todos.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code = 404, detail='To do not found')
    db.delete(todo)
    db.commit()
    return JSONResponse(status_code=200, content={'message' : 'To do deleted successfully'})


@app.get('/user')
def get_user(user : user_dependency, db : db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    return db.query(Users).filter(Users.id == user.get('user_id')).first()