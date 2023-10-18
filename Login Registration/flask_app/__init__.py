
from flask import Flask
from flask_bcrypt import Bcrypt        
app = Flask(__name__)
app.secret_key = "Nobody will know, how would they know?"
bcrypt = Bcrypt(app) 


DATABASE = "login_and_register_db"
