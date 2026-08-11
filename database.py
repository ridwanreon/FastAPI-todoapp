from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


#  ETA MYSQL ER JONNO:
# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:password@127.0.0.1:3306/todosapplicationdatabase'
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False,bind=engine)

Base = declarative_base()








# #  ETA POSTGRESQL ER JONNO :
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@localhost/TodoApplicationDatabase'

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal = sessionmaker(autoflush=False, autocommit=False,bind=engine)

# Base = declarative_base()



#  ETA SQLITE3 DATABASE ER JONNO: 

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'

# engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread':False})

# SessionLocal = sessionmaker(autoflush=False, autocommit=False,bind = engine)
# Base = declarative_base()







