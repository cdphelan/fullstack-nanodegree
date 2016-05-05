import sys

#comes in handy for mapper code
from sqlalchemy import Column, ForeignKey, Integer, String

#will use in configuration and class code
from sqlalchemy.ext.declarative import declarative_base

#for creating foreign keys, used in mapper
from sqlalchemy.orm import relationship

#used in config code at end of file
from sqlalchemy import create_engine

#making instance of declarative base class
#lets sqlach know they're special sqlalc classes
Base = declarative_base()

class Genre(Base):
	__tablename__ = 'genre'

	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)

	@property
	def serialize(self):
		return {
			'name': self.name,
			'id': self.id,
		}

#why can't do an inheritance of Genre here?
class Subgenre(Base):
	__tablename__ = 'subgenre'

	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)

	cat_code = Column(Integer)

	genre_id = Column(Integer, ForeignKey('genre.id'))
	genre = relationship(Genre)

	@property
	def serialize(self):
		return {
			'name': self.name,
			'id': self.id,
			'parent_genre_name': self.genre.name,
			'parent_genre_id': self.genre.id
		}

class Book(Base):
	__tablename__ = 'book'

	name = Column(String(80), nullable=False)
	id = Column(Integer, primary_key=True)

	author = Column(String(250))
	description = Column(String(250)) 
	pub_year = Column(String(4))

	subgenre_id = Column(Integer, ForeignKey('subgenre.id'))
	subgenre = relationship(Subgenre)

	@property
	def serialize(self):
		return {
			'name': self.name,
			'id': self.id,
			'author': self.author,
			'pub_year': self.pub_year,
			'description': self.description
		}

##config 
engine = create_engine('sqlite:///booklist.db')

Base.metadata.create_all(engine)