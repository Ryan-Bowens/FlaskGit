
from flask import Flask
app = Flask(__name__)
app.secret_key = "Nobody will know, how would they know?"

DATABASE = "user_db"