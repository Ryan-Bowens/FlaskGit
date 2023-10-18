# import the function that will return an instance of a connection
from flask_app.config.mysqlconnections import connectToMySQL
from flask_app import DATABASE, bcrypt
from flask import flash, session
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
# model the class after the user table from our database
class User:
    def __init__( self , data:dict ):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        #Add additional columns from database here

#CREATE
    @classmethod
    def create(cls, data:dict) -> int:
        query = "INSERT INTO user (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        id = connectToMySQL(DATABASE).query_db(query, data)
        return id


    @classmethod
    def get_one_by_email(cls, data:dict):
        """
        the data disctionary needs a key of 'email'
        """
        query = "SELECT * FROM user WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if not results:
            return []
        
        instance_list = []

        for dict in results:
            instance_list.append(dict)
        print(instance_list[0]['first_name'])
        return instance_list


#VALIDATE
    @staticmethod
    def validate(data:dict) -> bool:
        is_valid = True
#Column1
        if (len(data['first_name']) < 2):
            flash("first_name is required, must be 2 characters or more", "err_user_first_name")
            is_valid = False
#Column2
        if (len(data['last_name']) < 2):
            flash("last_name is required, must be 2 characters or more", "err_user_last_name")
            is_valid = False
#Email (Column3)
        if (len(data['email']) <= 7):
            flash("email is required, must be 7 characters or more", "err_user_email")
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!", "err_user_email")
        else:
            potential_user = User.get_one_by_email(data)
            if potential_user:
                flash("Email address already exists!", "err_user_email")
                is_valid = False
#Column 4
        if (len(data['password']) <= 8):
            flash("password is required, must be 8 characters or more", "err_user_password")
            is_valid = False

        if (len(data['confirm_password']) <= 8):
            flash("confirm_password is required, must be 8 characters or more", "err_user_confirm_password")
            is_valid = False

        elif data['password'] != data['confirm_password']:
            flash("Password and Confirm Password do not match", "err_user_confirm_password")
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(data:dict) -> bool:
        is_valid = True

        potential_user = User.get_one_by_email(data)

        if (len(data['email']) <= 7):
            flash("Email cannot be blank", "err_user_email")
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!", "err_user_email")
        else:
            if not potential_user:
                flash("Invalid Credentials!", "err_user_password_login")
                is_valid = False

        if (len(data['password']) <= 8):
            flash("Missing Password", "err_user_password")
            is_valid = False

        if is_valid:
            if not bcrypt.check_password_hash(potential_user[0]['password'], data['password']):
                flash("Invalid Credentials!", "err_user_password_login")
                is_valid = False
            else:
                session['uuid'] = potential_user[0]['id']

        return is_valid
