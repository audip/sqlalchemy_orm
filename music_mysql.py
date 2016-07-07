from connect_mysql import session, engine
from sqlalchemy import Column, Date, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
import datetime

Base = declarative_base()


def setup_tables():
    Base.metadata.create_all(engine)


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True)
    name = Column(String(25))

    def __init__(self, name):
        self.name = name


class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True)
    title = Column(String(25))
    release_date = Column(Date)
    publisher = Column(String(50))
    media_type = Column(String(40))

    artist_id = Column(Integer, ForeignKey("artists.id"))
    artist = relationship("Artist", backref=backref("albums", order_by=id))

    def __init__(self, title, release_date, publisher, media_type):
        self.title = title
        self.release_date = release_date
        self.publisher = publisher
        self.media_type = media_type


def add_collection():
    new_artist = Artist("Newsboys")
    new_artist.albums = [Album("Hell is for Wimps", datetime.date(1990, 07, 31), "Star Song", "CD"),
                         Album("Love Liberty Disco", datetime.date(1999,11,16), "Sparrow", "CD"),
                         Album("Thrive", datetime.date(2002,03,26), "Sparrow", "CD")]
    last_album = [Album("Read All About It",
                           datetime.date(1988,12,01),
                           "Refuge", "CD")]
    new_artist.albums.extend(last_album)
    session.add(new_artist)


def fetch_modify_album():
    res = session.query(Album).join(Artist).filter(Artist.name=="Newsboys").first()
    #print "<Title: %s, date: %s>" % (res.title, res.release_date)
    res.title = "Hell Is For Wimps"


if __name__ == '__main__':
    setup_tables()
    add_collection()
    fetch_modify_album()
    session.commit()
