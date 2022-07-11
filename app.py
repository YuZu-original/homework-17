from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

from app.models import Movie, MovieSchema, Director, DirectorSchema, Genre, GenreSchema
from app.setup_db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False}

db.init_app(app)
app.app_context().push()

api = Api(app)
movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@movie_ns.route('/')
@movie_ns.param('director_id', "director's ID",)
@movie_ns.param('genre_id', "genre's ID")
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get("director_id", type=int)
        genre_id = request.args.get("genre_id", type=int)
        
        if director_id and genre_id:
            movies = Movie.query.filter(Movie.director_id == director_id, Movie.genre_id == genre_id).all()
            return movies_schema.dump(movies), 200
        
        if director_id:
            movies = Movie.query.filter(Movie.director_id == director_id).all()
            return movies_schema.dump(movies), 200
        
        if genre_id:
            movies = Movie.query.filter(Movie.genre_id == genre_id).all()
            return movies_schema.dump(movies), 200
        
        movies = Movie.query.all()
        return movies_schema.dump(movies), 200
    
    
    def post(self):
        data = request.json
        new_movie = Movie(**data)
        with db.session.begin():
            db.session.add(new_movie)
        return "", 201


@movie_ns.route('/<int:pk>')
class MovieView(Resource):
    def get(self, pk):
        movie = Movie.query.get(pk)
        return movie_schema.dump(movie), 200

    def put(self, pk):
        movie = Movie.query.get(pk)
        req_data = request.json
        movie.title = req_data.get("title")
        movie.description = req_data.get("description")
        movie.trailer = req_data.get("trailer")
        movie.year = req_data.get("year")
        movie.rating = req_data.get("rating")
        movie.genre_id = req_data.get("genre_id")
        movie.director_id = req_data.get("director_id")
        db.session.add(movie)
        db.session.commit()
        return "", 204

    def delete(self, pk):
        movie = Movie.query.get(pk)
        if not movie:
            return "", 204
        db.session.delete(movie)
        db.session.commit()


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors = Director.query.all()
        return directors_schema.dump(directors), 200
    
    def post(self):
        data = request.json
        new_director = Director(**data)
        with db.session.begin():
            db.session.add(new_director)
        return "", 201


@director_ns.route('/<int:pk>')
class DirectorView(Resource):
    def get(self, pk):
        director = Director.query.get(pk)
        return director_schema.dump(director), 200
    
    def put(self, pk):
        director = Director.query.get(pk)
        req_data = request.json
        director.name = req_data.get("name")
        db.session.add(director)
        db.session.commit()
        return "", 204

    def delete(self, pk):
        director = Director.query.get(pk)
        if not director:
            return "", 204
        db.session.delete(director)
        db.session.commit()


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        genres = Genre.query.all()
        return genres_schema.dump(genres), 200
    
    def post(self):
        data = request.json
        new_genre = Genre(**data)
        with db.session.begin():
            db.session.add(new_genre)
        return "", 201


@genre_ns.route('/<int:pk>')
class GenreView(Resource):
    def get(self, pk):
        genre = Genre.query.get(pk)
        return genre_schema.dump(genre), 200

    def put(self, pk):
        genre = Genre.query.get(pk)
        req_data = request.json
        genre.name = req_data.get("name")
        db.session.add(genre)
        db.session.commit()
        return "", 204

    def delete(self, pk):
        genre = Genre.query.get(pk)
        if not genre:
            return "", 204
        db.session.delete(genre)
        db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)