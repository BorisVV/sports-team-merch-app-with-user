
from datetime import datetime
from sqlalchemy.engine import Engine
from sqlalchemy import \
            ForeignKey, event, create_engine, Column,\
            Integer, String, Float, DateTime
from sqlalchemy.orm import \
            relationship, sessionmaker, scoped_session, backref
from sqlalchemy.ext.declarative import declarative_base

from flask import url_for, Markup

from app_sport_team import app

# This block set up the relationship between tables for the ForeignKey.
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], convert_unicode=True)
# The scoped_session is good for queries managment.
db_session = scoped_session(sessionmaker(autoflush=False, bind=engine))

def init_db():
    Base.metadata.create_all(bind=engine)

# This set up the Base for the classes, engine to communicate with the db, and Session
# to bind the engine (open and close the sessions.)
Base = declarative_base()
Base.query = db_session.query_property()

class MerchandiseItems(Base):
    ''' This class is for the brand for the merchandises'''
    # Name of table
    __tablename__ = 'items'
    id = Column(Integer, primary_key = True)
    name = Column(String(50), unique=True, nullable = False)

    # Another option.
    # items = relationship('MerchandiseItems', backref=backref('sold', uselist=True, cascade='delete,all'))
    # cascade='all, delete-orphan', single_parent=True, passive_deletes=True)

    def __repr__(self):
        ''' Display the names list'''
        return '{}'.format(self.name)



class SoldRecords(Base):
    ''' This table is for the items sold in each game'''
    __tablename__ = 'sold'

    id = Column(Integer, primary_key = True)
    item_id = Column(Integer, ForeignKey('items.id'))
    date_id = Column(Integer, ForeignKey('schedules.id'))
    qty = Column(Integer)
    price = Column(Float(2))

    # tables relations.
    items = relationship('MerchandiseItems', backref=backref('sold', lazy='joined'))# ondelete='CASCADE'
    schedules = relationship('GamesDates', backref=backref('sold', lazy='joined'))

    def totalCost(self):
        return round((self.qty * self.price), 2)

    @property
    def url(self):
        return url_for('editSoldRecords', id=self.id)

    def __repr__(self):
        return "{} {}".format(self.qty, self.price)


class GamesDates(Base):
    ''' This will store the game's dates table'''
    __tablename__ = 'schedules'
    # Add columns
    id = Column(Integer, primary_key = True)
    _date = Column(DateTime, unique=True)
    city = Column(String(50))
    state = Column(String(50))

    @property
    def url(self):
        return url_for('editDates', id=self.id)

    def __repr__(self):
        return "{} {} {}".format(self._date, self.city, self.state)

init_db()
