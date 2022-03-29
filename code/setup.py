from flask_login import LoginManager , UserMixin , logout_user,login_user , current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, flash , redirect, request
from timest import *
app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_f.db'
dab = SQLAlchemy(app)
login_manager=LoginManager(app)
login_manager.init_app(app)
login_manager.login_view='home'
