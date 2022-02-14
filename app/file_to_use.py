from datetime import datetime
import os
from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)

print(basedir)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'books.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_ECHO']=True

# flask_restx
api = Api(app,doc='/',title="RestXApi", description='A simple Book API')

endpoints = api.namespace('books', description='books operations')

db=SQLAlchemy(app)

class Book(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    title=db.Column(db.String(80),nullable=False)
    author=db.Column(db.String(50),nullable=False)
    date_added=db.Column(db.String(50), default=datetime.utcnow)

    def __repr__(self):
        return self.title


book_model = api.model('Book', {
    'id': fields.Integer(),
    'title': fields.String(),
    'author': fields.String(),
    'date_added': fields.String()
})


@endpoints.route('/books')
class Books(Resource):
    @endpoints.doc('get all books')
    @endpoints.marshal_list_with(book_model,code=200,envelope="Book")
    def get_all_books(self):
        books = Books.query.all()
        return books

    def post_a_book(self):
        data= request.get_json()
        title = data.get('title')
        author = data.get('author')
        new_book = Book(title=title,author=author)
        db.session.add(new_book)
        db.session.commit()
        return new_book

@endpoints.route('/book<int:id>')
class BookResource(Resource):
    @endpoints.marshal_with(book_model,code=200,envelope="Book")
    def get_book_by_id(self,id):
        book = Book.get_or_404(id)
        return book,200
    
    @endpoints.marshal_with(book_model,code=200,envelope="Book")
    def update_book_by_id(self,id):
        book_to_update = Book.query.get_or_404(id)
        data = request.get_json()
        book_to_update.title = data.get('title')
        book_to_update.author = data.get('author')
        db.session.commit()
        return book_to_update,200

    @endpoints.marshal_with(book_model,code=200,envelope="Book")
    def delete_book_by_id(self,id):
        book_to_delete = Book.query.get_or_404(id)
        db.session.delete(book_to_delete)
        db.session.commit()
        return book_to_delete

# @endpoints.shell_context_processor
# def make_shell_context():
#     return{
#         'db':db,
#         'Book':Book
#     }