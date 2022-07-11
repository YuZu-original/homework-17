from flask_restx import Namespace, Resource, fields
from flask import request
from app.models import Genre, GenreSchema
from app.setup_db import db



api = Namespace('genres')

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)



@api.route('/')
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


@api.route('/<int:pk>')
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