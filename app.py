# For flask object
from flask import Flask, render_template, url_for, redirect, request, flash

# for sqlalchemy ORM
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from wtforms_sqlalchemy.fields import QuerySelectField
from pprint import pprint
from forms import *
# Flask object
app = Flask(__name__)

# Configs
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "mysecretkey"

########################## MODELS (DATABASE FORMATION)
# database object inherit app object as superclass
db = SQLAlchemy(app)
# For migration
# Migrate with app,db as super classes
Migrate(app,db)

"""
for automation i might create a separate file.
for now i do it manually

    1)set FLASK_APP=app.py #-- script that holds the app and db (with any file structure)
    2)flask db init creates migration file structure
    3)ipytohn db.create_all() to create tables
    #-- First time and after any changes in db structure:
    1)flask db migrate -m "message" to migrate
    2)flask db upgrade
"""
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True, nullable=False)
    author = db.Column(db.String())
    quantity = db.Column(db.Integer())
    price = db.Column(db.Integer)

    #-- for debuging later on ill cheng it to __str__
    def __repr__(self):
        return f"{self.title} | {self.author} | {self.price} | {self.quantity}"

#-- Instead of creating methods i use separate functions
def get_id(title):
    book = Book.query.filter_by(title=title).first()
    return book.id

def insert_record(title, author, quantity, price):
    new_book = Book(title=title, author=author, quantity=quantity, price=price)
    db.session.add(new_book)
    db.session.commit()

def remove_record(id):
    book = Book.query.filter_by(id=id).first()
    if book is None:
        print("Record not found")
    else:
        db.session.delete(book)
        db.session.commit()

def update_record(id,title,author,quantity,price):
    book = Book.query.filter_by(id=id).first()
    book.title = title
    book.author = author
    book.quantity = quantity
    book.price = price
    db.session.commit()


def show_all():
    all_books = Book.query.all()
    return all_books

def search_record_by_title(title):
    book = Book.query.filter_by(title=title).all()
    return book

def search_records_by_author(author):
    books = Book.query.filter_by(author=author).all()
    return books

def search_records_by_quantity(quantity):
    books = Book.query.filter_by(quantity=quantity).all()
    return books

def search_records_by_price(price):
    books = Book.query.filter_by(price=price).all()
    return books

def book(id):
    book = Book.query.filter_by(id=id).first()
    return book

########################### Routes

##########################  HOME
@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    form = SelectForm()
    all_books = show_all()
    return render_template("home.html", all_books=all_books, form=form)

######################### SELECT FIELDS
@app.route("/<id>", methods = ["GET", "POST"])
def id(id):
    book = Book.query.filter_by(id=id).first()
    form = SelectForm(title=book.title, author=book.author, quantity=book.quantity, price=book.price)

    if form.validate_on_submit():
        if form.delete.data:
            remove_record(id=id)
            return home()
        elif form.update.data:
            title = form.title.data
            author = form.author.data
            quantity = form.quantity.data
            price = form.price.data
            update_record(id,title,author,quantity,price)
            return home()
    return render_template("id.html", form=form)

#########################  INSERT
#-- insert new records to database
@app.route("/insert", methods=["GET", "POST"])
def insert():
    #-- form object from form class
    form = InsertForm()

    if form.validate_on_submit():
        title = form.title.data
        author = form.author.data
        quantity = form.quantity.data
        price = form.price.data
        insert_record(title,author,quantity,price)
        flash("Record Created Successfully")
        return home()
    return render_template("insert.html", form=form)

#########################  REMOVE
#-- should move the link to info page with connector to given list object
@app.route("/remove", methods=["GET","POST"])
def remove():
    return render_template("remove.html")

#########################  UPDATE
#-- should move the link to info page with connector to given list object
@app.route("/update", methods=["GET","POST"])
def update():
    return render_template("update.html")

#--Maybe I'll use difflib and SequenceMatcher to improve the search
#########################  SEARCH BY TITLE
# basic search for title
@app.route("/search_by_title", methods=["GET","POST"])
def search_by_title():
    form = SearchTitleForm()
    if form.validate_on_submit():
        title = form.title.data
        result = search_record_by_title(title)
        return render_template("result.html", result=result)
    return render_template("search_by_title.html", form=form)

#########################  SEARCH BY AUTHOR
@app.route("/search_by_author", methods=["GET","POST"])
def search_by_author():
    form = SearchAuthorForm()
    if form.validate_on_submit():
        author = form.author.data
        result = search_records_by_author(author)
        return render_template("result.html", result=result)
    return render_template("search_by_author.html", form=form)

#########################  SEARCH BY QUANTITY
@app.route("/search_by_quantity", methods=["GET","POST"])
def search_by_quantity():
    form = SearchQuantityForm()
    if form.validate_on_submit():
        quantity = form.quantity.data
        result = search_records_by_quantity(quantity)
        return render_template("result.html", result=result)
    return render_template("search_by_quantity.html", form=form)

#########################  SEARCH BY PRICE
@app.route("/search_by_price", methods=["GET","POST"])
def search_by_price():
    form = SearchPriceForm()
    if form.validate_on_submit():
        price = form.price.data
        result = search_records_by_price(price)
        return render_template("result.html", result=result)
    return render_template("search_by_price.html", form=form)

if __name__ == '__main__':
    app.run()
