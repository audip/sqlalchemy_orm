from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import ConfigParser


config = ConfigParser.ConfigParser()
config.read("config.cnf")
url = config.get('MySQL', 'DBURL')
engine = create_engine(url, echo=True)
Session = sessionmaker(bind=engine)
session = Session()