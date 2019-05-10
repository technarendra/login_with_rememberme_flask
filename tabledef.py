from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///database.db', echo=True)
Base = declarative_base()
 
########################################################################
class User(Base):
	""""""
	__tablename__ = "user"
	 
	id = Column(Integer, primary_key=True)
	username = Column('username', String(20), unique=True , index=True)
	password = Column('password', String(10))
	email = Column('email', String(50),unique=True , index=True)
	active = Column(Boolean(), nullable=False, server_default='0')

	def get_id(self):
		return unicode(self.alternative_id)
 
#----------------------------------------------------------------------
def __init__(self , username ,password , email):
	self.username = username
	self.password = password
	self.email = email
	self.registered_on = datetime.utcnow()



# create tables
Base.metadata.create_all(engine)

