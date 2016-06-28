from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from connecting import session, engine


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(50))

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % \
               (self.name, self.fullname, self.password)
    
def create_tables():
    Base.metadata.create_all(engine)

def create_users():
    new_user = User(name='Aditya', fullname='Aditya Purandare', password='password')
    session.add(new_user)
    session.add_all([
        User(name='wendy', fullname='Wendy Williams', password='foobar'),
        User(name='mary', fullname='Mary Contrary', password='xxg527'),
        User(name='fred', fullname='Fred Flinstone', password='blah')])
    new_user.password = 'strongpassword'

def fetch_user():
    fetched_user = session.query(User).filter_by(name='Aditya').first()
    print "<User(name='%s', fullname='%s', password='%s')>" % \
          (fetched_user.name, fetched_user.fullname, fetched_user.password)

def fetch_users():
    fetched_users = session.query(User).all()
    for each_user in fetched_users:
        print "<User(name='%s', fullname='%s', password='%s')>" % \
              (each_user.name, each_user.fullname, each_user.password)

if __name__ == '__main__':
    create_tables()
    create_users()
    fetch_users()
    session.commit()
