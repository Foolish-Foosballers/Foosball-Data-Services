from flask import Flask
from datetime import date, datetime
from flask_sqlalchemy import SQLAlchemy
import os, json, logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
from models import *

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.DEBUG)

def createTables():
    app.logger.debug('creating tables')
    db.create_all()
    app.logger.debug('created tables')

def dropTables():
    app.logger.debug('dropping tables')
    db.drop_all()
    app.logger.debug('dropped tables')

def jsonSerial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

@app.route('/')
def homepage():
    # dropTables()
    # createTables()

    # player = Player(Id=0, FirstName="Daniel", LastName="Lerner",
    # Username="dlernz", Email="daniel.lerner@ge.com")
    # db.session.add(player)
    # player = Player(Id=1, FirstName="Sara", LastName="Stik",
    # Username="sarastik", Email="sara.stik@ge.com")
    # db.session.add(player)
    # player = Player(Id=2, FirstName="Brett", LastName="Oberg",
    # Username="wisco", Email="brett.oberg@ge.com")
    # db.session.add(player)
    # db.session.commit()

    output = Player.query.get(0)
    app.logger.debug(output.FirstName)
    output = Player.query.get(1)
    app.logger.debug(output.FirstName)
    output = Player.query.get(2)
    app.logger.debug(output.FirstName)
    
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>

    <img src="http://loremflickr.com/600/400">
    """.format(time=the_time)

@app.route('/players')
def players():
    players = Player.query.all()
    return json.dumps([player.as_dict() for player in players], default=jsonSerial)

@app.route('/players/<id>')
def playersById(id):
    player = Player.query.get_or_404(id)
    return json.dumps(player.as_dict(), default=jsonSerial)

@app.route('/players/<username>')
def playersByUsername(username):
    player = Player.query.filter_by(Username=username).first_or_404()
    return json.dumps(player.as_dict(), default=jsonSerial)

@app.route('/games')
def games():
    games = Games.query.all()
    return json.dumps([game.as_dict() for game in games], default=jsonSerial)

@app.route('/games/<id>')
def gamesById(id):
    game = Game.query.get_or_404(id)
    return json.dumps(player.as_dict(), default=jsonSerial)

if __name__ == '__main__':
    app.run()
