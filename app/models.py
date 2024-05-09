from sqlalchemy import create_engine, Column, Integer, String, Text, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Config

Base = declarative_base()


class Card(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    tag = Column(String(255))
    ability = Column(Text)
    cost = Column(Integer)
    power = Column(Integer)
    img = Column(Text)
    keywords = Column(ARRAY(String))

    def __repr__(self):
        return f"<Card(name='{self.name}', tag='{self.tag}, ability={self.ability}, "\
            f"cost={self.cost}, power={self.power}, img={self.img}, keywords={self.keywords})>"


engine = create_engine(Config.DB_URI)
Session = sessionmaker(bind=engine)


def storage(cards):
    session = Session()

    for card in cards:
        existing_card = session.query(Card).filter_by(name=card.name).first()
        if existing_card:
            if (existing_card.tag, existing_card.ability, existing_card.cost, existing_card.power, existing_card.img, existing_card.keywords) != (card.tag, card.ability, card.cost, card.power, card.img, card.keywords):
                existing_card.tag = card.tag
                existing_card.ability = card.ability
                existing_card.cost = card.cost
                existing_card.power = card.power
                existing_card.img = card.img
                existing_card.keywords = card.keywords
        else:
            new_card = Card(name=card.name, tag=card.tag, ability=card.ability,
                            cost=card.cost, power=card.power, img=card.img, keywords=card.keywords)
            session.add(new_card)

    session.commit()
    session.close()
