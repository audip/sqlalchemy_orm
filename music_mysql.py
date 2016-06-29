from connect_mysql import session, engine
from sqlalchemy import Column, Date, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
Base = declarative_base()

def create_tables():
    Base.metadata.create_all(engine)
 
########################################################################
class Artist(Base):
    """"""
    __tablename__ = "artists"
 
    id = Column(Integer, primary_key=True)
    name = Column(String(25))
 
    #----------------------------------------------------------------------
    def __init__(self, name):
        """"""
        self.name = name    
 
########################################################################
class Album(Base):
    """"""
    __tablename__ = "albums"
 
    id = Column(Integer, primary_key=True)
    title = Column(String(25))
    release_date = Column(Date)
    publisher = Column(String(50))
    media_type = Column(String(40))
 
    artist_id = Column(Integer, ForeignKey("artists.id"))
    artist = relationship("Artist", backref=backref("albums", order_by=id))
 
    #----------------------------------------------------------------------
    def __init__(self, title, release_date, publisher, media_type):
        """"""
        self.title = title
        self.release_date = release_date
        self.publisher = publisher
        self.media_type = media_type

if __name__=='__main__':
    create_tables()