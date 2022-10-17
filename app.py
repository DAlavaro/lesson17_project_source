# app.py

from flask import request
from flask_restx import Resource

from config import api, app, db
from models import Movie, Genre, Director
from schema import MovieSchema, GenreSchema, DirectorSchema


movie_ns = api.namespace("movies")
movies_schema = MovieSchema()
movies_schemas = MovieSchema(many=True)

genre_ns = api.namespace('genres')
genre_schema = GenreSchema()
genre_schemas = GenreSchema(many=True)

director_ns = api.namespace('directors')
director_schema = DirectorSchema()
director_schemas = DirectorSchema(many=True)


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
            return "Данные изменены", 201
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


@director_ns.route('/')
class DirectorsView(Resource):
    def post(self):
        """
        Формирование представления для добавления нового режиссера
        """

        json_req = request.json
        director_added = Director(**json_req)
        db.session.add(director_added)
        db.session.commit()
        return '', 201


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did):
        try:
            director = Director.query.filter(Director.id == did).one()
        except Exception as e:
            return f'{e}', 404
        return director_schema.dump(director)

    def put(self, did):
        director = Director.query.get(did)
        if not director:
            return '', 404

        json_req = request.json
        director.name = json_req.get("name")
        db.session.add(director)
        db.session.commit()
        return '', 204

    def delete(self, did):
        """
        Формирование представления для удалени режиссера по id
        В случае отсутствия режиссера - ошибка
        """

        director = Director.query.get(did)
        if not director:
            return '', 404
        db.session.delete(director)
        db.session.commit()
        return '', 204


@genre_ns.route('/')
class GenresView(Resource):
    def post(self):
        json_req = request.json
        genre_added = Genre(**json_req)
        db.session.add(genre_added)
        db.session.commit()
        return '', 201



@genre_ns.route('/<int:did>')
class GenreView(Resource):
    def get(self, did):
        try:
            genre = Genre.query.filter(Genre.id == did).one()
        except Exception as e:
            return f'{e}', 404
        return genre_schema.dump(genre)

    def put(self, did):
        genre = Genre.query.get(did)
        if not genre:
            return '', 404

        json_req = request.json
        genre.name = json_req.get("name")
        db.session.add(genre)
        db.session.commit()
        return '', 204

    def delete(self, did):
        genre = Genre.query.get(did)
        if not genre:
            return '', 404
        db.session.delete(genre)
        db.session.commit()
        return '', 204


if __name__ == '__main__':
    app.run(debug=True)
