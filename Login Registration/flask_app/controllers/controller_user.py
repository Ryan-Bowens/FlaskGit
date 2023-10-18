from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.model_user import User
from flask_app.__init__ import bcrypt

@app.route('/')
def starting():
    if 'uuid' in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    #If user id is not in session (prevents going directly to /dashboard)
    # if not 'uuid' in session:
    #     return redirect('/')
    
    loggedin_user = User.get_one({'id': session['uuid']})
    return render_template('dashboard.html', loggedin_user=loggedin_user)

@app.post('/register')
def register():
    #Validate
    print(request.form)
    if User.validate(request.form) == False:
        print('Registration Failed')
        return redirect('/')
    
    #set up hash
    hash_pw = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password': hash_pw
    }

    #create user
    id = User.create(data)

    #store id into session
    session['uuid'] = id

    return redirect('/dashboard')

@app.post('/login')
def login():
    if User.validate_login(request.form) == True:
        print('success')
        return redirect('/dashboard')
    print('else')
    return redirect('/')

@app.post('/logout')
def logout():
    del session['uuid']
    return redirect('/')

