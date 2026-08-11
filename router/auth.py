from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel,Field
from typing import Annotated,Optional
from datetime import timedelta,datetime,timezone
from sqlalchemy.orm import Session
from models import Users
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from database import SessionLocal
from jose import jwt 

from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer

router = APIRouter()




bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated = 'auto')
OAuth2_bearer = OAuth2PasswordBearer(tokenUrl='login')





SECRET_KEY = 'c0b3005dcdadd57742d6319a116720b9e65ecb9ff0a8ebf8a504df40b975010b'
ALGORITHM = 'HS256'





class CreateUsers(BaseModel):
    email : str
    username : str
    firstname : str
    lastname : str
    password : str
    role : str
    Phone_number : str



class UpdateUser(BaseModel):
    email : Optional[str] = Field(default=None)
    username : Optional[str] = Field(default=None)
    firstname : Optional[str] = Field(default=None)
    lastname : Optional[str] = Field(default=None)
    Phone_number : Optional[str] = Field(default=None)
    
class UpdatePassword(BaseModel):
    current_password : str
    new_password : str





def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def authenticate_user(username,password,db):
    user = db.query(Users).filter(Users.username == username).first()
    if user is None:
        return False
    
    if bcrypt_context.verify(password, user.hash_passsword):
        
        return user
    return False
        



def create_access_token(username : str, user_id : int, role : str, expires_delta : timedelta):
    encode = {'sub': username, 'id' : user_id, 'role' : role}
    expire = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp' : expire})
    return jwt.encode(encode,SECRET_KEY,algorithm = ALGORITHM)





def get_current_user(Token : Annotated[str, Depends(OAuth2_bearer)]):
    
    try:
        payload = jwt.decode(Token,SECRET_KEY,algorithms=[ALGORITHM])
        username : str = payload.get('sub')
        user_id : int = payload.get('id')
        role : str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=404, detail='User not found')
        
        return {'user_name' : username, 'user_id' : user_id, 'role' : role}
    except:
        raise HTTPException(status_code=404, detail='User not found')
       
       
       
       
       
db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]






@router.post('/createusers')
def create_users(db :db_dependency,new_user : CreateUsers):
    user_model = Users(
        email = new_user.email,
        username = new_user.username,
        firstname = new_user.firstname,
        lastname = new_user.lastname,
        hash_passsword = bcrypt_context.hash(new_user.password),
        is_active = True,
        role = new_user.role,
        Phone_number = new_user.Phone_number
       )
    
    db.add(user_model)
    db.commit()

    return JSONResponse(status_code=201, content={'message' : 'Create users successfully'})
   
   
   
   
@router.post('/login')
def login_user(db : db_dependency, form_data : Annotated[OAuth2PasswordRequestForm,Depends()]):
    user = authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=401, detail='Failed Authentication')
    
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=30))
    return {'access_token' : token, 'token_type' : 'bearer'}


@router.put('/edituser')
def Update_User(user : user_dependency, db : db_dependency, update_user : UpdateUser):
    if user is None:
        raise HTTPException(status_code=401, detail='Failed Authentication')
    
    User = db.query(Users).filter(Users.id == user.get('user_id')).first()
    
    updateuser = update_user.model_dump(exclude_unset=True)
    
    for key,value in updateuser.items():
        setattr(User,key,value)
        
    db.commit()
    return JSONResponse(status_code=200, content={'message' : 'User updated successfully'})


@router.put('/passwordchange')
def Update_User(user : user_dependency, db : db_dependency, update_password : UpdatePassword):
    
    if user is None:
        raise HTTPException(status_code=401, detail='Failed Authentication')
    
    User = db.query(Users).filter(Users.id == user.get('user_id')).first()
    
    if not bcrypt_context.verify(update_password.current_password,User.hash_passsword):
        raise HTTPException(status_code=401, detail='Wrong password')
    User.hash_passsword = bcrypt_context.hash(update_password.new_password)
    
    db.add(User)  
    db.commit()
    return JSONResponse(status_code=200, content={'message' : 'Password change successfully'})