from flask_app.config.mysqlconnections import connectToMySQL
from flask_app import DATABASE

# model the class after the dojos table from our database
# WARNING!!! DONT IMPORT THE CLASS IMPORT THE FILE
from flask_app.models import model_ninjas

class Dojos:
    def __init__( self , data:dict ):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        self.ninjas=[]

    @classmethod
    def save (cls, data):
        query = "INSERT INTO dojo"


#CREATE
    @classmethod
    def create(cls, data:dict) -> int:
        query = "INSERT INTO dojo_and_ninjas_schema.dojos (name) VALUES (%(name)s);"
        id = connectToMySQL(DATABASE).query_db(query, data)
        return id

#GET ALL
# get_all()
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls) -> list:
        """
        Explain What this function does
        This function gets all the dojos from the database and
        reutnrs a list of INSTANCES!!. It doesn't recquire any
        parameters.
        """
        query = "SELECT * FROM dojos;"

        #returns a LIST of DICTIONARIES !OR! FALSE
        results = connectToMySQL(DATABASE).query_db(query)
        # Shield!!! False, []
        if not results:
            return []
        
        instance_list = []
        for dict in results:
        
            instance_list.append(cls(dict))

        return instance_list

#GET ONE
    @classmethod
    def get_one(cls, data:dict):
        """
        data dictionary needs a key of 'id'
        """
        query = "SELECT * FROM dojo_and_ninjas_schema.dojos WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if not results:
            return []
        
        dict = results[0]
        instance = cls(dict)
        return instance
