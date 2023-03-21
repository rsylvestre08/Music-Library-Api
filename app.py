from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api, Resource
from dotenv import load_dotenv
from os import environ

load_dotenv()

# Create App instance
app = Flask(__name__)

# Add DB URI from .env
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')

# Registering App w/ Services
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
CORS(app)
Migrate(app, db)

# Models
class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    album = db.Column(db.String(255), nullable=False)
    release_date = db.Column(db.Date)
    genre = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'{self.title} {self.artist} {self.album} {self.release_date} {self.genre}'
  
# Schemas
class Create_songSchema(ma.Schema):
    class Meta:
        fields = ("id.", "title", "artist", "album", "release_date", "genre")

create_song_schema = Create_songSchema()
create_songs_schema = Create_songSchema(many=True)

# Resources
class MusicListResource(Resource):
    def get(self):
        all_music = Music.query.all()
        return create_songs_schema.dump(all_music)
    
    def post(self):
        print(request)
        new_music = Music(
            title=request.json['title'],  
            artist=request.json['artist'],
            album=request.json['album'],
            release_date=request.json['release_date'],
            genre=request.json['genre']
        )
        db.session.add(new_music)
        db.session.commit()
        return create_song_schema.dump(new_music), 201

class MusicResource(Resource): 
    def get(self, song_id):
        song_from_db = Music.query.get_or_404(song_id)
        return create_song_schema.dump(song_from_db)
        
    def delete(self,song_id):    
        song_from_db = Music.query.get_or_404(song_id)
        db.session.delete(song_from_db)
        return '', 204
    
    def put(self, song_id):
        song_from_db = Music.query.get_or_404(song_id)

        if 'title' in request.json:
            song_from_db.title =request.json['title']
        if 'artist' in request.json:
            song_from_db.artist =request.json['artist']
        if 'album' in request.json:
            song_from_db.album =request.json['album']
        if 'release_date' in request.json:
            song_from_db.release_date =request.json['release_date']
        if 'genre' in request.json:
            song_from_db.genre =request.json['genre']
        db.session.commit()
        return create_song_schema.dump(song_from_db)


# Routes
api.add_resource(MusicListResource, '/api/songs') 
api.add_resource(MusicResource, '/api/songs/<int:song_id>')  
 
