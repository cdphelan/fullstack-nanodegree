from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import csv
 
from database_setup import Base, Genre, Subgenre, Book
 
engine = create_engine('sqlite:///booklist.db')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# create genres (categories)
#Parent genres
supgenres = {'Human': [1,2,3],
			'Natural': [4,5],
			'Supernatural': [6,7,8],
			'Unexplained': [9]}

#Subgenres
genres = {1:'Nuclear war',
		2: 'Social collapse', 
		3: 'Plague, etc.',
		4: 'Terrestrial', 
		5: 'Cosmic',
		6: 'Zombies',
		7: 'Aliens, monsters',
		8: 'Divine',
		9: 'Unexplained'}

#Add parent genres to db
for s in supgenres:
	genre = Genre(name=s)
	session.add(genre)
session.commit()

#Add subgenres to db
for g in genres:
	genre = None
	for k,v in supgenres.items():
		if g in v:
			genre = session.query(Genre).filter_by(name=k).first()
	subgenre = Subgenre(name = genres[g], cat_code=g, genre=genre)
	session.add(subgenre)
session.commit()

#Add books to db
with open('apocalypse-books.csv', 'rU') as csvfile:
	reader = csv.reader(csvfile)
	next(reader,None)
	for line in reader:
		c = int(line[3])
		subgenre = session.query(Subgenre).filter_by(cat_code=c).first()
		book = Book(name=line[0], 
					author=line[1], 
					pub_year=line[2], 
					description=None, 
					subgenre=subgenre)
		session.add(book)
session.commit()

print 'added books!'