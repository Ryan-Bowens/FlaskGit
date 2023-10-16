from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.model_dojos import Dojos
from flask_app.models.model_ninjas import Ninjas

#DISPLAY ROUTE
@app.route('/dojos')
def dojos_show():
    all_dojos = Dojos.get_all()
    return render_template('dojos.html', all_dojos=all_dojos)

#ACTION ROUTE
@app.post('/dojos/create')
def dojos_create():
    Dojos.create(request.form)
    return redirect('/dojos')

#DISPLAY ROUTE
@app.route('/dojos/<int:id>')
def dojos_show_one(id):
    data = {
        'id': id
    }
    dojos = Dojos.get_one(data)
    dojo_ninjas = Ninjas.get_dojo(data)
    return render_template('dojos_show_one.html', dojos=dojos, dojo_ninjas=dojo_ninjas)

#DISPLAY ROUTE
@app.route('/ninjas/new')
def ninja_new():
    all_dojos = Dojos.get_all()
    return render_template('ninjas_create.html', all_dojos=all_dojos)

#ACTION ROUTE
@app.post('/ninjas/create')
def ninja_create():
    Ninjas.create(request.form)
    return redirect('/dojos')

