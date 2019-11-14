from flask_login import UserMixin
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

from main import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    firstname = db.Column(db.String(80))
    secondname = db.Column(db.String(80))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    groups = db.Column(db.String(80))
    id_ref = db.Column(db.Integer,nullable=True)
    rub = db.Column(db.Integer)
    usd = db.Column(db.Integer)

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    firstname = StringField('firstname', validators=[InputRequired(), Length(min=1, max=80)])
    secondname = StringField('secondname', validators=[InputRequired(), Length(min=1, max=80)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=80)])
    groups = StringField('groups')
    ref = StringField('ref')

	
class MainPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    low_price = db.Column(db.Float)

class Competitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comp_name = db.Column(db.String)
    name = db.Column(db.String)
    low_price = db.Column(db.Float)
	

class Words(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    words = db.Column(db.String, unique=True)

class SearchQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.String, unique=True)
	
	
class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    selected_record = db.Column(db.String, unique=True)
    main_records = db.Column(db.Text)
    competitor_records = db.Column(db.Text)



# Мега костыль для нормальной поддержки UTF8
from sqlalchemy.event import listen

db_collate = 'ru_RU.UTF-8'   # RU language for example
def load_extension(dbapi_conn, unused):
    dbapi_conn.enable_load_extension(True)             # aptitude install libicu-dev libsqlite3-dev build-essential
    dbapi_conn.load_extension('./libSqliteIcu.arm.so') # под другую платформу надо пересобрать gcc -shared icu.c `icu-config --ldflags` -fPIC -o libSqliteIcu.so
    dbapi_conn.enable_load_extension(False)
    dbapi_conn.execute("SELECT icu_load_collation(?, 'ICU_EXT_1')", (db_collate,))
with app.app_context():
    listen(db.engine, 'connect', load_extension)
	
	
	
	
db.create_all()