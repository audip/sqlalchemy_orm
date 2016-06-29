from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, or_, ForeignKey
from connecting import session, engine
from sqlalchemy.orm import backref, relationship


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

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", backref=backref('addresses', order_by=id))

def create_tables():
    Base.metadata.create_all(engine)

def create_users():
    new_user = User(name='Aditya', fullname='Aditya Purandare', password='password')
    new_user.addresses = [Address(email_address='aditya@email.com'), Address(email_address='aditya@hello.com')]
    second_user = User(name='wendy', fullname='Wendy Williams', password='foobar')
    session.add(new_user)
    session.add(second_user)
    session.add_all([
        User(name='mary', fullname='Mary Contrary', password='xxg527'),
        User(name='fred', fullname='Fred Flinstone', password='blah')])
    new_user.password = 'strongpassword'
    session.delete(second_user)

def fetch_user():
    #fetched_user = session.query(User).filter_by(name='Aditya').first()
    fetched_user = session.query(User).filter(or_(User.name.like('%Ad%')), User.fullname != 'Anand').one()
    another_user = session.query(User).join(Address).filter(Address.email_address=='aditya@email.com').all()
    print "<User(name='%s', fullname='%s', password='%s', email_address='%s')>" % \
          (fetched_user.name, fetched_user.fullname, fetched_user.password, fetched_user.addresses)
    print "Another User: %s" % (another_user)

def fetch_users():
    fetched_users = session.query(User).all()
    print "No. of users fetched: %d " % (session.query(User).count())
    for each_user in fetched_users:
        print "<User(name='%s', fullname='%s', password='%s')>" % \
              (each_user.name, each_user.fullname, each_user.password)

if __name__ == '__main__':
    create_tables()
    create_users()
    print "Fetch a user: %s" % (fetch_user())
    print "Fetching users: %s" % (fetch_users())
    session.commit()
    session.close()

