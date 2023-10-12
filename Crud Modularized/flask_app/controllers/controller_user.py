from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.model_user import User


#DISPLAY ROUTE -> Shows the form to create a user
@app.route('/user/new')
def user_new():
    return render_template('user_new.html')

#ACTION ROUTE -> process the form from the new route (above)
@app.post('/user/create')
def user_create():
    User.create(request.form)
    return redirect('/users')

#DISPLAY ROUTE -> display all
@app.route('/users')
def user_show():
    all_users = User.get_all()
    return render_template('user_show.html', all_users=all_users)

#DISPLAY ROUTE -> just display the user info
@app.route('/user/<int:id>')
def user_show_one(id):
    user = User.get_one({'id': id})
    return render_template('user_show_one.html', user=user)

#DISPLAY ROUTE -> display the form to edit the user
@app.route('/user/<int:id>/edit')
def user_edit(id):
    user_edit = User.get_one({'id': id})
    return render_template('user_edit.html', user=user_edit)

#ACTION ROUTE -> process the form from the edit route
@app.post('/user/<int:id>/update')
def user_update(id):
    data = {
        "id": id,
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email']
    }
    User.update(data) # User.update(request.form) works with <input type="hidden" name="id" value="{{user.id}}">
    return redirect('/users')

#ACTION ROUTE -> delete the record from the database
@app.post('/user/<int:id>/delete')
def user_delete(id):
    User.delete_one({'id': id})
    return redirect('/users')