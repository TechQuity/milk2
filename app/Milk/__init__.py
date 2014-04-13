from flask import Flask
 
app = Flask(__name__)

app.secret_key = 'thisisthetestkey'

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'echotest245@gmail.com'  
app.config["MAIL_PASSWORD"] = 'Apple123456'
 
 
from routes import mail
mail.init_app(app)
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1:3306/milk'
 
from models import db
db.init_app(app)
 
import Milk.routes