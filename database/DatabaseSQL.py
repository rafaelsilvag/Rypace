__author__ = 'Rafael S. Guimaraes'

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationships
from config import RypaceConfigParser

configParser = RypaceConfigParser.RypaceConfigParser()
configDB = configParser.readDBConfig()


if configDB:
    if configDB['dbms']:
        engine = create_engine(configDB['dbms']+'://'+configDB['username']+
                               '@'+configDB['hostname']+'/'+configDB['database'])
else:
    engine = create_engine('mysql://root@127.0.0.1/openflow')

Base = declarative_base()
Session = sessionmaker(bind=engine)

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    role = Column(String)
    created = Column(Date)
    modified = Column(Date)

    def __repr__(self):
        return "<User: ('%s','%s')>" % (self.id, self.username)

class Blacklists(Base):
    __tablename__ = 'blacklists'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    descricao = Column(String)
    created = Column(Date)
    modified = Column(Date)

    def __repr__(self):
        return "<Blacklist: ('%s','%s')>" % (self.id, self.descricao)

class Ips(Base):
    __tablename__ = 'ips'
    id = Column(Integer, primary_key=True)
    ip = Column(String)
    blacklist_id = Column(Integer, ForeignKey(Blacklists.id))
    created = Column(Date)
    modified = Column(Date)

    def __repr__(self):
        return "<IPs: ('%s','%s', '%s')>" % (self.ip, self.blacklist_id, self.created)

class Controls(Base):
    __tablename__ = 'controls'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(Users.id))
    mac = Column(String)
    created = Column(Date)
    modified = Column(Date)

    def __repr__(self):
        return "<Controls: ('%s','%s')>" % (self.id, self.mac)

class ControlsBlacklists(Base):
    __tablename__ = 'controls_blacklists'
    id = Column(Integer, primary_key=True)
    blacklist_id = Column(Integer, ForeignKey(Blacklists.id))
    controls_id = Column(Integer, ForeignKey(Controls.id))
    created = Column(Date)
    modified = Column(Date)
    def __repr__(self):
        return "<ControlsBlacklists: ('%s','%s')>" % (self.blacklist_id, self.controls_id)

class Hours(Base):
    __tablename__ = 'hour'
    id = Column(Integer, primary_key=True)
    hour_start = Column(Time)
    hour_stop = Column(Time)
    description = Column(String)
    controls_id = Column(Integer, ForeignKey(Controls.id))
