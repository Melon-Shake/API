from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

db_url = "postgresql://{username}:{password}@{host}:{port}/{dbname}".format(
    username='postgres',
    password='12345678',
    host='database-1.coea55uwjt5p.ap-northeast-1.rds.amazonaws.com',
    port='5432',
    dbname=''
)
engine = create_engine(db_url, echo=True, connect_args={'sslmode':'require'})

Session = sessionmaker(bind=engine, autoflush=True, autocommit=False)
@contextmanager
def session_scope() :
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
    pass

if __name__ == '__main__' :
    mapper = inspect(engine)
    for tb in mapper.get_table_names() :
        print(tb)