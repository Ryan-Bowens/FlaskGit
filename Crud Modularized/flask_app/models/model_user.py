# import the function that will return an instance of a connection
from flask_app.config.mysqlconnections import connectToMySQL
from flask_app import DATABASE
# model the class after the table from our database
class User:
    def __init__( self , data:dict ):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.email = data['email']
        self.first_name = data['first_name']
        self.last_name = data['last_name']

    # def info(self): 
    #     returnStr = f"Name = {self.name} || Age = {self.age} || Breed = {self.breed}"
    #     return returnStr
    

#CREATE
# create()
    @classmethod
    def create(cls, data:dict):
        query = "INSERT INTO user (email, first_name, last_name) VALUES (%(email)s, %(first_name)s, %(last_name)s);"
        id = connectToMySQL(DATABASE).query_db(query, data)
        return id

#GET ALL
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls) -> list:
        """
        Explain What this function does
        This function gets all the user from the database and
        reutnrs a list of INSTANCES!!. It doesn't recquire any
        parameters.
        """
        query = "SELECT * FROM user;"
        # make sure to call the connectToMySQL function with the schema you are targeting.

        #returns a LIST of DICTIONARIES !OR! FALSE
        results = connectToMySQL(DATABASE).query_db(query)
        # Create an empty list to append our instances of friends
        
        # Shield!!! False, []
        if not results:
            return []
        

        instance_list = []
        # Iterate over the db results and create instances of friends with cls.
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
        query = "SELECT * FROM user WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if not results:
            return []
        
        dict = results[0]
        instance = cls(dict)
        return instance

#UPDATE
    @classmethod
    def update(cls, data:dict):
        query = "UPDATE user SET email = %(email)s, first_name = %(first_name)s, last_name = %(last_name)s WHERE id = %(id)s;"
        id = connectToMySQL(DATABASE).query_db(query, data)
        return id

#DELETE
    @classmethod
    def delete_one(cls, data:dict):
        """
        data dictionary needs a key of 'id'
        """
        query = "DELETE FROM user WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)
