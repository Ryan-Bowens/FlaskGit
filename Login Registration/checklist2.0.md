6. create my file structure
    1. Root folder (Name of Project)
        1. Flask_app
            1. config
                1. mysqlconnection.py
            2. controllers
                1. controller_animal.py
            3. models
                1. model_animal.py
            4. static
                1. css
                    1. style.css
                2. js
                    1. script.js
            5. templates
                1. index.html
            6. \_\_init__.py
        2. pipfile
        3. pipfile.lock
        4. server.py
7. add boilerplate code
8. Test to make sure server is working

# My File boilerplates

BCRYPT
suggests putting it in init, file too small
call upon it in controller 



python -m pipenv install flask,
python -m pipenv install flask pymysql,
pipenv install flask-bcrypt (if needed),
python -m pipenv shell,
python server.py,




## mysqlconnections.py
```py

# a cursor is the object we use to interact with the database
import pymysql.cursors
# this class will give us an instance of a connection to our database
class MySQLConnection:
    def __init__(self, db):
        # change the user and password as needed
        connection = pymysql.connect(host = 'localhost',
                                    user = 'root', 
                                    password = 'root', 
                                    db = db,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor,
                                    autocommit = False)
        # establish the connection to the database
        self.connection = connection
    # the method to query the database
    def query_db(self, query:str, data:dict=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
     
                cursor.execute(query)
                if query.lower().find("insert") >= 0:
                    # INSERT queries will return the ID NUMBER of the row inserted
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # SELECT queries will return the data from the database as a LIST OF DICTIONARIES
                    result = cursor.fetchall()
                    return result
                else:
                    # UPDATE and DELETE queries will return nothing
                    self.connection.commit()
            except Exception as e:
                # if the query fails the method will return FALSE
                print("********Something went wrong********", e)
                return False
            finally:
                # close the connection
                self.connection.close() 
# connectToMySQL receives the database we're using and uses it to create an instance of MySQLConnection
def connectToMySQL(db):
    return MySQLConnection(db)
    
```


## server.py FILE
```py

from flask_app import app
from flask_app.controllers import controller_TABLE_NAME


if __name__ =="__main__":
    app.run(debug=True)

```


## __init__.py FILE
```py

from flask import Flask
from flask_bcrypt import Bcrypt        
app = Flask(__name__)
app.secret_key = "Nobody will know, how would they know?"
bcrypt = Bcrypt(app) 


DATABASE = "database name here (sql)"

```


## model.py FILE
```py

# import the function that will return an instance of a connection
from flask_app.config.mysqlconnections import connectToMySQL
from flask_app import DATABASE
# model the class after the animal table from our database
class <TABLE_NAME>:
    def __init__( self , data:dict ):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        #Add additional columns from database here

    # def info(self): 
    #     returnStr = f"Name = {self.name} || Age = {self.age} || Breed = {self.breed}"
    #     return returnStr
    

#CREATE
    @classmethod
    def create(cls, data:dict) -> int:
        query = "INSERT INTO TABLE_NAME (column1, column2, column3, column4) VALUES (%(column1)s, %(column2)s, %(column3)s, %(column4)s);"
        id = connectToMySQL(DATABASE).query_db(query, data)
        return id

#GET ALL
# get_all()
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls) -> list:
        """
        Explain What this function does
        This function gets all the TABLE_NAME from the database and
        returns a list of INSTANCES!!. It doesn't recquire any
        parameters.
        """
        query = "SELECT * FROM TABLE_NAME;"

        #returns a LIST of DICTIONARIES !OR! FALSE
        results = connectToMySQL(DATABASE).query_db(query)
        # Shield!!! False, []
        if not results:
            return []
        
        instance_list = []

        for dict in results:
            #    empty list       class -> instance
            instance_list.append( cls(dict) )
        return instance_list
            

#GET ONE
    @classmethod
    def get_one(cls, data:dict):
        """
        data dictionary needs a key of 'id'
        """
        query = "SELECT * FROM table_name WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if not results:
            return []
        
        dict = results[0]
        instance = cls(dict)
        return instance

#UPDATE
    @classmethod
    def update(cls, data:dict):
        query = "UPDATE table_name SET column1 = %(column1)s, column2 = %(column2)s, column3 = %(column3)s WHERE id = %(id)s;"
        id = connectToMySQL(DATABASE).query_db(query, data)
        return id

#DELETE
    @classmethod
    def delete_one(cls, data:dict):
        """
        data dictionary needs a key of 'id'
        """
        query = "DELETE FROM table_name WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

#VALIDATE
    @staticmethod
    def validate(data:dict) -> bool:
        is_valid = True
#Column1
        if (len(data['column1']) < 2):
            flash("column1 is required, must be 2 characters or more", "err_users_column1")
            is_valid = False
#Column2
        if (len(data['column2']) < 2):
            flash("column2 is required, must be 2 characters or more", "err_users_column2")
            is_valid = False
#Email (Column3)
        if (len(data['email']) <= 7):
            flash("email is required, must be 7 characters or more", "err_users_email")
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!", "err_users_email")
        else:
            potential_user = User.get_one_by_email(data)
            if potential_user:
                flash("Email address already exists!", "err_users_email")
            is_valid = False
#Column 4
        if (len(data['password']) <= 8):
            flash("password is required, must be 8 characters or more", "err_users_password")
            is_valid = False

        if (len(data['confirm_password']) <= 8):
            flash("confirm_password is required, must be 8 characters or more", "err_users_confirm_password")
            is_valid = False

        elif data['password'] != data['confirm_password']:
            flash("Password and Confirm Password do not match", "err_users_confirm_password")
            is_valid = False

#Validate Login
    @staticmethod
    def validate_login(data:dict) -> bool:
        is_valid = True

        if (len(data['email']) <= 7):
            flash("email is required, must be 7 characters or more", "err_users_email")
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!", "err_users_email")
        else:
            potential_user = User.get_one_by_email(data)
            if not potential_user:
                flash("Invalid Credentials!", "err_users_password_login")
            is_valid = False

        if (len(data['password']) <= 8):
            flash("password is required, must be 8 characters or more", "err_users_password")
            is_valid = False

        if is_valid:
            if not bcrypt.check_password_hash(potential_user.password, data['password']):
                flash("Invalid Credentials!", "err_users_password_login")
                is_valid = False
            else:
                session['uuid'] = potential_user.id

        return is_valid
```


## controller_"table".py FILE
```py
from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.model_<table_name> import <Class_Name>

# /table_name/id?/action
# /table_name/new
# /table_name/create
# /table_name/<int:id>
# /table_name/<int:id>/edit
# /table_name/<int:id>/update
# /table_name/<int:id>/delete

@app.route('/')
def starting():
    return render_template('index.html')

#DISPLAY ROUTE -> Shows the form to create a <table_name>
@app.route('/<table_name>/new')
def <table_name>_new():
    return render_template('<table_name>_new.html')

#ACTION ROUTE -> process the form from the new route (above)
@app.post('/<table_name>/create')
def <table_name>_create():
    <Class_name>.create(request.form)
    return redirect('/')
    # Redirect to All <table_name> for instance

    #DISPLAY ROUTE -> display all
@app.route('/table_name(s)')
def <table_name>_show():
    all_<table_name>s = <Class_Name>.get_all()
    return render_template('<table_name>_show.html', all_<table_name>s=all_<table_name>s)

#DISPLAY ROUTE -> just display the <table_name> info
@app.route('/<table_name>/<int:id>')
def <table_name>_show_one(id):
    <table_name> = <Class_name>.get_one({'id': id})
    return render_template('<table_name>_show_one.html', <table_name>=<table_name>)

#DISPLAY ROUTE -> display the form to edit the <table_name>
@app.route('/<table_name>/<int:id>/edit')
def <table_name>_edit(id):
    <table_name>_edit = <Class_Name>.get_one({'id': id})
    return render_template('<table_name>_edit.html', <table_name>=<table_name>_edit)

#ACTION ROUTE -> process the form from the edit route
@app.post('/<table_name>/<int:id>/update')
def <table_name>_update(id):
    data = {
        "id": id,
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email']
    }
    <Class_Name>.update(data) # <Class_Name>.update(request.form) works with <input type="hidden" name="id" value="{{<table_name>.id}}">
    return redirect('/table_name(s)')

#ACTION ROUTE -> delete the record from the database
@app.post('/<table_name>/<int:id>/delete')
def <table_name>_delete(id):
    <Class_Name>.delete_one({'id': id})
    return redirect('/table_name(s)')

```

## HTML template FILE

```html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Game Demo</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <h1>Index</h1>

    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>

```

## HTML login form 

```html

```

## HTML registration form
```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User New</title>
</head>

<body>
    <form action="/table_name/create" method="post">
        <h1>Add table_name/h1>
        <p>First Name: {{first_name}}
            <input type='text' name="first_name">
        </p>
        <p>Last Name: {{last_name}}
            <input type='text' name="last_name">
        </p>
        <p>Email: {{email}}
            <input type='text' name="email">
        </p>
        <a href="/table_name(s)"><button id="Submit">Submit</button></a>
    </form>
    <a href="/table_name(s)">List of all users</a>
</body>
<!-- Substitute name="" values -->
</html>
```




#Look at Video 
#     #Instance of the
        #     dojos_instance = cls(dict)
            
        # #1 Extract our ninjas data
        #     ninjas_data= {
        #         **dict,
            
        #         #conflicting columns
        #         'id': dict['ninjas.id'],
        #         'created_at': dict['ninjas.created_at'],
        #         'updated_at': dict['ninjas.updated_at'],

        #         # #non-conflicting columns
        #         # 'first_name': dict['ninjas.first_name'],
        #         # 'last_name': dict['ninjas.last_name'],
        #         # 'age': dict['ninjas.age']
        #     }

        #     #2 Make a ninjas instance
        #     ninjas_instance = model_ninjas.Ninjas(ninjas_data)

        #     #3 attach the ninjas instance ot the dojos_instance
        #     dojos_instance.ninja_person = ninjas_instance
        #     dojos_instance.bananas = "lets go bananas"

        #     #Take the instance and add it to the list "instance_list"