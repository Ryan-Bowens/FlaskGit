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
                ```py
                from flask import Flask
                    app = Flask (__name__)
                    app.secret_key = 'keep it secret, keep it safe'
                    from flask_bcrypt import Bcrypt
                ```
        2. pipfile
        3. pipfile.lock
        4. server.py
7. add boilerplate code
8. Test to make sure server is working

# My File boilerplates

BCRYPT
suggests putting it in init, file too small
call upon it in controller 



python -m pipenv install flask
python -m pipenv install flask pymysql
python -m pipenv shell
python server.py




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
app = Flask(__name__)
app.secret_key = "Nobody will know, how would they know?"


DATABASE = "database name here (sql)"

```


## model.py FILE
```py

# import the function that will return an instance of a connection
from flask_app.config.mysqlconnections import connectToMySQL
from flask_app import DATABASE
# model the class after the animal table from our database
class Animal:
    def __init__( self , data:dict ):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        #Add additional columns from database here

    # def info(self): 
    #     returnStr = f"Name = {self.name} || Age = {self.age} || Breed = {self.breed}"
    #     return returnStr
    

#CREATE
# create()
    @classmethod
    def create_one(cls, data:dict) -> int:
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
        reutnrs a list of INSTANCES!!. It doesn't recquire any
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
#get_one()
    @classmethod
    def get_one(cls, data:dict):
        query = "SELECT * FROM TABLE_NAME WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        
        if not results:
            return []

#UPDATE
# update_one()

#DELETE
# delete_one()
    @classmethod
    def delete_one(cls, data:dict):
        """
        data dictionary needs a key of 'id'
        """
        query = "DELETE FROM TABLE_NAME WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)


```


## controller_"table".py FILE
```py
from flask_app import render_template, redirect, request, session
from flask_app import app
from flask_app.models.model_TABLE_NAME import CLASS_NAME_Upper

# /table_name/id?/action
# /table_name/new
# /table_name/create
# /table_name/<int:id>
# /table_name/<int:id>/edit
# /table_name/<int:id>/update
# /table_name/<int:id>/delete

#DISPLAY ROUTE -> Shows the form to create a CLASS_NAME
@app.route('/CLASS_NAME_lower/new')
def CLASS_NAME_lower_new():
    return render_template('CLASS_NAME_lower_new.html')

#ACTION ROUTE -> process the form from the new route (above)
@app.post('/CLASS_NAME_lower/create')
def CLASS_NAME_lower_create():
    CLASS_NAME.create(request.form)
    return redirect('/')
    # Redirect to All TABLE_NAME for instance

    #DISPLAY ROUTE -> display all
@app.route('/TABLE_NAMEs')
def user_show():
    all_users = User.get_all()
    return render_template('user_show.html', all_users=all_users)

#DISPLAY ROUTE -> just display the CLASS_NAME info
@app.route('/CLASS_NAME_lower/<int:id>')
def CLASS_NAME_lower_show(id):
    CLASS_NAME_lower = CLASS_NAME_lower.get_one({'id': id})
    return render_template('CLASS_NAME_lower_show.html')

#DISPLAY ROUTE -> display the form to edit the CLASS_NAME
@app.route('/CLASS_NAME_lower/<int:id>/edit')
def CLASS_NAME_lower_edit(id):
    CLASS_NAME_lower_edit = CLASS_NAME_Upper.get_one({'id': id})
    return render_template('CLASS_NAME_lower_edit.html', CLASS_NAME_lower=CLASS_NAME_lower_edit)

#ACTION ROUTE -> process the form from the edit route
@app.post('/CLASS_NAME_lower/<int:id>/update')
def CLASS_NAME_lower_update(id):
    data = {
        "id": id,
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email']
    }
    CLASS_NAME_Upper.update(data) # User.update(request.form) works with <input type="hidden" name="id" value="{{user.id}}">
    return redirect('/TABLE_NAMEs')

#ACTION ROUTE -> delete the record from the database
@app.post('/CLASS_NAME_lower/<int:id>/delete')
def CLASS_NAME_lower_delete(id):
    CLASS_NAME_Upper.delete_one({'id': id})
    return redirect('/TABLE_NAMEs')

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
    <form action="/TABLE_NAME/create" method="post">
        <h1>Add TABLE_NAME</h1>
        <p>First Name: {{first_name}}
            <input type='text' name="first_name">
        </p>
        <p>Last Name: {{last_name}}
            <input type='text' name="last_name">
        </p>
        <p>Email: {{email}}
            <input type='text' name="email">
        </p>
        <a href="/TABLE_NAMEs"><button id="Submit">Submit</button></a>
    </form>
    <a href="/users">List of all users</a>
</body>
<!-- Substitute name="" values -->
</html>
```