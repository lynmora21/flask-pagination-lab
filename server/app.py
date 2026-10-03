#!/usr/bin/env python3

from flask import request, session, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

import os
from config import create_app, db, api
from models import Book, BookSchema

env = os.getenv("FLASK_ENV", "dev")
app = create_app(env)
api.init_app(app)


class Books(Resource):
    def get(self):
        # Get pagination parameters from the request URL.
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        # Fetch only the requested page of books.
        # error_out=False returns an empty list for pages beyond the last page.
        pagination = Book.query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        books = [BookSchema().dump(book) for book in pagination.items]

        return {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "total_pages": pagination.pages,
            "items": books
        }, 200


api.add_resource(Books, '/books', endpoint='books')
api.init_app(app)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
