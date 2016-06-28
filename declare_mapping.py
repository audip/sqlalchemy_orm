from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from connecting import engine


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(50))

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)

Base.metadata.create_all(engine)
a_user = User(name='Aditya', fullname='Aditya Purandare', password='password')
print "<User(name='%s', fullname='%s', password='%s')>" % (a_user.name, a_user.fullname, a_user.password)