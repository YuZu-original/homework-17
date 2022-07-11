from flask_restx import Namespace, Resource, fields
from flask import request
from app.models import Movie, MovieSchema
from app.setup_db import db



api = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@api.route('/')
@api.param('director_id', "director's ID",)
@api.param('genre_id', "genre's ID")
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


@api.route('/<int:pk>')
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