from sqlalchemy import Column, Integer, String, ForeignKey, func, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker


Base = declarative_base()
engine = create_engine('mysql://root:@192.168.14.4/sqlalchemy', echo=True, pool_recycle=3600)
Session = sessionmaker(bind=engine)
session = Session()


def setup_tables():

    Base.metadata.create_all(engine)

    # Add dream team for mock data
    session.add_all([
        Player("Aditya", 10, "forward"),
        Player("Ronaldo", 7, "forward"),
        Player("Bale", 11, "forward"),
        Player("Hulk", 12, "forward"),
        Player("Rooney", 9, "midfield"),
        Player("Messi", 8, "midfield"),
        Player("Ibrahimovic", 5, "midfield"),
        Player("Iniesta", 6, "midfield"),
        Player("Smalling", 3, "defense"),
        Player("De Gea", 1, "defense"),
        Player("Pepe", 2, "defense"),
        Player("Darmian", 4, "defense")
    ])
    session.commit()


class Player(Base):
    """ A pool of players (say 26) in a team """
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    jersey_number = Column(Integer, unique=True)
    position = Column(String(20))

    def __init__(self, name, jersey_number, position):
        self.name = name
        self.jersey_number = jersey_number
        self.position = position


class Squad(Base):
    """ Only 11 fit players are selected """
    __tablename__ = "squad"

    id = Column(Integer, primary_key=True)
    squad_jersey_number = Column(Integer, ForeignKey('players.jersey_number'))
    squad_position = Column(String(20), ForeignKey('players.position'))

    def __init__(self, jersey_number, position):
        self.squad_jersey_number = jersey_number
        self.squad_position = position


def insert_player(jersey_number):
    # check_position for player
    res = session.query(Player).filter(Player.jersey_number == jersey_number).first()
    pos = res.position
    if check_positions(pos):
        player_info = session.query(Player).filter(Player.position == pos).\
            filter(Player.jersey_number == jersey_number).first()
        # Add player to table
        fresh_player = Squad(player_info.jersey_number, player_info.position)
        session.add(fresh_player)


def remove_player(jersey_number):
    # delete the player
    tired_player = session.query(Squad).filter(Squad.squad_jersey_number == jersey_number).first()
    session.delete(tired_player)


def check_positions(position):
    # return true if player can be added, false otherwise
    formation = {
        'forward': 3,
        'midfield': 4,
        'defense': 4}
    position_count = session.query(Squad).filter(Squad.squad_position == position).count()

    if formation[position] > position_count:
        return True
    else:
        return False


if __name__ == '__main__':
    # setup_tables()

    insert_player(1)
    insert_player(2)
    insert_player(3)
    insert_player(4)
    insert_player(5)
    insert_player(6)
    insert_player(7)
    insert_player(8)
    insert_player(9)
    insert_player(10)
    insert_player(11)

    session.commit()

    remove_player(11)
    insert_player(12)

    session.commit()

    session.close()
