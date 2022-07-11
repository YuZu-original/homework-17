from flask_restx import Namespace, Resource, fields
from flask import request
from app.models import Director, DirectorSchema
from app.setup_db import db



api = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)



@api.route('/')
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


@api.route('/<int:pk>')
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