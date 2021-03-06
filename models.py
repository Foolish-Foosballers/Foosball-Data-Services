from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db
import enum

class TableSide(enum.Enum):
    LEFT = "Left"
    RIGHT = "Right"

class Players(db.Model):
    Id = db.Column(db.Integer, primary_key=True, nullable=False)
    FirstName = db.Column(db.String(120), nullable=False)
    LastName = db.Column(db.String(120), nullable=False)
    Username = db.Column(db.String(9), unique=True, nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    SignupDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    TotalTimePlayed = db.Column(db.Integer, nullable=False, default=0)
    GameWins = db.Column(db.Integer, nullable=False, default=0)
    TotalGamesPlayed = db.Column(db.Integer, nullable=False, default=0)
    SeriesWins = db.Column(db.Integer, nullable=False, default=0)
    TotalPoints = db.Column(db.Integer, nullable=False, default=0)
    Shutouts = db.Column(db.Integer, nullable=False, default=0)
    Ranking = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, firstName, lastName, username, email):
        self.FirstName = firstName
        self.LastName = lastName
        self.Username = username
        self.Email = email
        self.SignupDate = datetime.now()
        self.TotalTimePlayed = 0
        self.GameWins = 0
        self.TotalGamesPlayed = 0
        self.SeriesWins = 0
        self.TotalPoints = 0
        self.Shutouts = 0
        self.Ranking = 0

    def as_dict(self):
        """Method for converting model to a dictionary for JSON serializable output"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Games(db.Model):
    Id = db.Column(db.Integer, primary_key=True, nullable=False)
    StartTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    Duration = db.Column(db.Integer, nullable=False)
    Single = db.Column(db.Boolean, nullable=False)
    LeftScore = db.Column(db.Integer, nullable=False)
    RightScore = db.Column(db.Integer, nullable=False)
    WinMargin = db.Column(db.Integer, nullable=False)
    Winner = db.Column(db.Enum(TableSide), nullable=False)

    def __init__(self, duration, single, leftScore, rightScore, winMargin, winner):
        self.StartTime = datetime.now() # JUST FOR TESTING PURPOSES
        self.Duration = duration
        self.Single = single
        self.LeftScore = leftScore
        self.RightScore = rightScore
        self.WinMargin = winMargin
        self.Winner = winner

    def as_dict(self):
        """Method for converting model to a dictionary for JSON serializable output"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Series(db.Model):
    Id = db.Column(db.Integer, primary_key=True, nullable=False)
    NumGames = db.Column(db.Integer, nullable=False)
    LeftWins = db.Column(db.Integer, nullable=False)
    RightWins = db.Column(db.Integer, nullable=False)

    def __init__(self, numGames, leftWins, rightWins):
        self.NumGames = numGames
        self.LeftWins = leftWins
        self.RightWins = rightWins

    def as_dict(self):
        """Method for converting model to a dictionary for JSON serializable output"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class History(db.Model):
    GameId = db.Column(db.Integer, db.ForeignKey('games.Id'), primary_key=True, nullable=False)
    PlayerId = db.Column(db.Integer, db.ForeignKey('players.Id'), primary_key=True, nullable=False)
    SeriesId = db.Column(db.Integer, db.ForeignKey('series.Id'), nullable=False)
    Side = db.Column(db.Enum(TableSide), nullable=False)

    def __init__(self, gameId, playerId, seriesId, side):
        self.GameId = gameId
        self.PlayerId = playerId
        self.SeriesId = seriesId
        self.Side = side

    def as_dict(self):
        """Method for converting model to a dictionary for JSON serializable output"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}