from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__,template_folder='templates',static_folder='static')
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)
login.login_view = 'login'
from app import routes,models
bootstrap = Bootstrap(app)
app.config['UPLOAD_FLODER']='/home/harshith/microblog/uploads'
app.config['MAX_CONTENT_LENGTH']=16*1024*1024