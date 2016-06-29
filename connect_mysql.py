from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('mysql+mysqldb://root:@192.168.14.4/sqlalchemy', echo=True, pool_recycle=3600)
Session = sessionmaker(bind=engine)
session = Session()