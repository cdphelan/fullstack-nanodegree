import random, string, httplib2, json, requests

from flask import Flask, render_template, request, redirect, url_for, flash
from flask import jsonify, make_response
from flask import session as login_session

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Genre, Subgenre, Book

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

###
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "udacity-catalog-cdp"

# connect to database and create session
engine = create_engine('sqlite:///booklist.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

### LOGIN PAGES ###

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

# CONNECT
@app.route('/gconnect', methods=['POST'])
def gconnect():

    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        print 'made it here'
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already'+
        'connected.'), 200)                    
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h2>Welcome, '
    output += login_session['username']
    output += '!</h2>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 100px; height: 100px;border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# DISCONNECT 
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['credentials']
    print 'In gdisconnect access token is %s' % access_token
    print 'User name is: ' 
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 
            401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s'%access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    print access_token
    if result['status'] == '200':
        del login_session['credentials'] 
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash("You have successfully been logged out.")
        return redirect(url_for('showGenres'))
    else:
        flash('Failed to revoke token for given user.')
        return redirect(url_for('showGenres'))

## PAGES ##
#GENRE & SUBGENRE PAGES

#view all
@app.route('/')
@app.route('/genres/')
def showGenres():
    genres = sorted(session.query(Genre).all(), key=lambda g: g.name)
    subgenres = session.query(Subgenre).all()
    random.shuffle(subgenres) #returns all the subgenres in random order
    return render_template('genres.html', genres=genres, subgenres=subgenres)

#Parent genres are not editable, so no add/edit/del behavior for them

#view all subgenres
@app.route('/genres/<int:genre_id>/')
def showSubgenres(genre_id):
    genres = sorted(session.query(Genre).all(), key=lambda g: g.name)
    genre = session.query(Genre).filter_by(id=genre_id).one()
    subgenres = session.query(Subgenre).filter_by(genre_id=genre_id).all()
    return render_template('subgenres.html', 
        genres=genres, genre=genre, subgenres=subgenres)

#add new subgenre
@app.route('/genre/<int:genre_id>/new', methods=['GET','POST'])
def newGenre(genre_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newGenre = Subgenre(name=request.form['name'],genre_id=genre_id)
        session.add(newGenre)
        session.commit()
        flash("New subgenre created")
        return redirect(url_for('showSubgenres', genre_id=genre_id))
    else:
        genre = session.query(Genre).filter_by(id=genre_id).one()
        return render_template('newgenre.html', 
            genre_id=genre_id, genre_name=genre.name)

#edit subgenre
@app.route('/genres/<int:subgenre_id>/edit', methods=['GET','POST'])
def editGenre(subgenre_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedGenre = session.query(Subgenre).filter_by(id=subgenre_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedGenre.name = request.form['name']
        session.add(editedGenre)
        session.commit()
        flash("Genre successfully edited")
        return redirect(url_for('showGenres'))
    else:
        return render_template('editgenre.html', 
            subgenre_id=subgenre_id, item=editedGenre)

#delete subgenre
@app.route('/genres/<int:subgenre_id>/delete/', methods=['GET','POST'])
def deleteGenre(subgenre_id):
    if 'username' not in login_session:
        return redirect('/login')
    deletedGenre = session.query(Subgenre).filter_by(id=subgenre_id).one()
    if request.method == 'POST':
        session.delete(deletedGenre)
        session.commit()
        flash("Genre successfully deleted")
        return redirect(url_for('showGenres'))
    else:
        return render_template('deletegenre.html', item=deletedGenre)

#BOOK PAGES
#view booklist
@app.route('/genres/<int:subgenre_id>/')
@app.route('/genres/<int:subgenre_id>/booklist')
def showBooklist(subgenre_id):
    genres = sorted(session.query(Genre).all(), key=lambda g: g.name)
    subgenre = session.query(Subgenre).filter_by(id=subgenre_id).one()
    items = session.query(Book).filter_by(subgenre_id=subgenre.id).all()
    return render_template('books.html', 
        genres=genres, subgenre=subgenre, items=items)

#add new book 
@app.route('/genres/<int:subgenre_id>/new', methods=['GET','POST'])
def newBook(subgenre_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newBook = Book(name=request.form['name'], 
            author=request.form['author'], 
            pub_year=request.form['pub_year'], 
            description=request.form['description'], 
            subgenre_id=subgenre_id)
        session.add(newBook)
        session.commit()
        flash("New book created")
        return redirect(url_for('showBooklist',subgenre_id=subgenre_id))
    else:
        return render_template('newbook.html', subgenre_id=subgenre_id)

#edit book
@app.route('/genres/<int:subgenre_id>/<int:book_id>/edit', 
    methods=['GET', 'POST'])
def editBook(subgenre_id, book_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Book).filter_by(id=book_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['author']:
            editedItem.author = request.form['author']
        if request.form['pub_year']:
            editedItem.pub_year = request.form['pub_year']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        flash("Book successfully edited")
        return redirect(url_for('showBooklist', subgenre_id=subgenre_id))
    else:
        return render_template('editBook.html', 
            subgenre_id=subgenre_id, BookID=book_id, item=editedItem)

#delete book
@app.route('/genres/<int:subgenre_id>/<int:book_id>/delete/', 
    methods=['GET', 'POST'])
def deleteBook(subgenre_id, book_id):
    if 'username' not in login_session:
        return redirect('/login')
    deletedItem = session.query(Book).filter_by(id=book_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash("Book successfully deleted")
        return redirect(url_for('showBooklist', subgenre_id=subgenre_id))
    else:
        return render_template('deleteBook.html', item=deletedItem)

#API endpoints
#all genres
@app.route('/genres/JSON')
def allGenresJSON():
    genres = session.query(Genre).all()
    return jsonify(Genres=[r.serialize for r in genres])

#all subgenres, with parent genre links
@app.route('/genres/subgenres/JSON')
def allSubgenresJSON():
    genres = session.query(Genre).all()
    subgenres = session.query(Subgenre).all()
    return jsonify(Subgenres=[r.serialize for r in subgenres])

#booklist for a specific subgenre
@app.route('/genres/<int:subgenre_id>/booklist/JSON')
def genrelistJSON(subgenre_id):
    genre = session.query(Subgenre).filter_by(id=subgenre_id).one()
    items = session.query(Book).filter_by(subgenre_id=subgenre_id).all()
    return jsonify(Books=[i.serialize for i in items])

#specific book
@app.route('/genres/<int:subgenre_id>/booklist/<int:book_id>/JSON')
def BookJSON(subgenre_id, book_id):
    item = session.query(Book).filter_by(id=book_id).one()
    return jsonify(Book=[item.serialize])

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
