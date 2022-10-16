# app.py

from flask import request
from flask_restx import Resource

from config import api, app, db
from models import Movie
from schema import MovieSchema


movie_ns = api.namespace("movies")
movies_schema = MovieSchema()
movies_schemas = MovieSchema(many=True)


@movie_ns.route("/")
class MovieViews(Resource):
    def get(self):
        query = Movie.query

        director_id = request.args.get('director_id')
        if director_id:
            query = query.filter(Movie.director_id == director_id)

        if genre_id := request.args.get('genre_id'):
            query = query.filter(Movie.genre_id == genre_id)

        return movies_schemas.dump(query)

    def post(self):
        data = request.json
        try:
            db.session.add(
                Movie(
                    **data
                )
            )
            db.session.commit()
            return "Данные добавлены", 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200


@movie_ns.route("/<int:mid>")
class MovieViews(Resource):
    def get(self, mid):
        query = Movie.query.get(mid)
        return movies_schema.dump(query)

    def put(self, mid):
        data = request.json

        try:
            db.session.query(Movie).filter(Movie.id == mid).update(
                data
            )
            db.session.commit()
            return "Данные обновлены", 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200


    def delete(self, mid):

        try:
            db.session.query(Movie).filter(Movie.id == mid).delete()
            db.session.commit()
            return "Данные удалены", 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200


if __name__ == '__main__':
    app.run(debug=True)
