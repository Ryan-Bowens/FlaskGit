from flask import render_template, redirect, request
from flask_app import app
from flask_app.models.model_ninjas import Ninjas
from flask_app.models.model_dojos import Dojos


@app.route('/')
def starting():
    return render_template('index.html')

