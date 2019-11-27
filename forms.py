from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from app import *


class InsertForm(FlaskForm):
    title = StringField("Title")
    author = StringField("Author")
    quantity = IntegerField("Quantity")
    price = IntegerField("Price")
    submit=SubmitField("INSERT")

class SearchTitleForm(FlaskForm):
    title = StringField("Title")
    submit = SubmitField("Search")

class SearchAuthorForm(FlaskForm):
    author = StringField("Author")
    submit = SubmitField("Search")

class SearchQuantityForm(FlaskForm):
    quantity = StringField("Quantity")
    submit = SubmitField("Search")

class SearchPriceForm(FlaskForm):
    price = StringField("Price")
    submit = SubmitField("Search")

class SelectForm(FlaskForm):
    title=StringField("Title")
    author=StringField("Author")
    quantity = IntegerField("Quantity")
    price = IntegerField("Price")
    update = SubmitField(label="UPDATE")
    delete = SubmitField(label="DELETE")
