from datetime import date, datetime
import os
from turtle import title
from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy

from app.file_to_use import Books


app = Flask(__name__)
api = Api(app, version='1.0', title='BookMVC API',
    description='A simple BookMVC API',
)

basedir = os.path.dirname(os.path.realpath(__file__))

endoint = api.namespace('Book', description='TODO operations on Book')

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///book.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_ECHO']=True

db=SQLAlchemy(app)

class Book(db.Model):
    book_id=db.Column(db.Integer(),primary_key=True)
    author=db.Column(db.String(80),nullable=False)
    country=db.Column(db.String(50),nullable=False)
    imageLink=db.Column(db.String(80),nullable=False)
    language=db.Column(db.String(20),nullable=False)
    link=db.Column(db.String(80),nullable=False)
    pages=db.Column(db.String(10),nullable=False)
    title=db.Column(db.String(50),nullable=False)
    year=db.Column(db.String(10),nullable=False)
    date_added=db.Column(db.String(20), default=date)

    def __init__(self,author,country,imageLink,language,link,pages,title,year,date):
        self.author = author
        self.country = country
        self.imageLink = imageLink
        self.language = language
        self.link = link
        self.pages = pages
        self.title = title
        self.year = year
        self.date_added = date

book_model = api.model('Book', {
    'book_id': fields.Integer(),
    'author': fields.String(),
    'country': fields.String(),
    'imageLink': fields.String(),
    'language': fields.String(),
    'link': fields.String(),
    'pages': fields.Integer(),
    'title': fields.String(),
    'year': fields.Integer(),
    'date_added': fields.Date()
})



@endoint.route('/')
class BookList(Resource):
    @endoint.marshal_list_with(book_model)
    def get(self):
        '''List all books'''
        books = Book.query.all()
        return books 

    @endoint.expect(book_model)
    @endoint.marshal_with(book_model, code=201)
    def post(self):
        '''Create a new book'''
        data = request.get_json()
        book_author = data.get('author')
        book_country = data.get('country')
        book_imageLink = data.get('imageLink')
        book_language = data.get('language')
        book_link = data.get('link')
        book_pages = data.get('pages')
        book_title = data.get('title')
        book_year = data.get('year')
        date_added = data.get('date_added')
        new_book = Book(
            author=book_author,
            country=book_country,
            imageLink=book_imageLink,
            language=book_language,
            link=book_link,
            pages=book_pages,
            title=book_title,
            year=book_year,
            date=date_added
        )
        db.session.add(new_book)
        db.session.commit()
        return new_book, 201
        # return DAO.create(api.payload), 201


@endoint.route('/<int:id>')
@endoint.response(404, 'Todo not found')
class Todo(Resource):
    @endoint.marshal_with(book_model)
    def get(self, id):
        '''Fetch a given resource'''
        book = Book.query.get(id)
        return book

    @endoint.response(204, 'Todo deleted')
    def delete(self, id):
        book_to_delete = Book.query.get(id)
        db.session.delete(book_to_delete)
        db.session.commit()
        return '', 204

    @endoint.expect(book_model)
    @endoint.marshal_with(book_model)
    def put(self, id):
        '''Update a task given its identifier'''
        book_to_update = Book.query.get(id)
        data = request.get_json()
        book_to_update.author = data.get('author')
        book_to_update.country = data.get('country')
        book_to_update.imageLink = data.get('imageLink')
        book_to_update.language = data.get('language')
        book_to_update.link = data.get('link')
        book_to_update.pages = data.get('pages')
        book_to_update.title = data.get('title')
        book_to_update.year = data.get('year')
        book_to_update.date_added = data.get('date_added')

        db.session.commit()
        return book_to_update, 200

       