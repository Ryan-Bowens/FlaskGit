from flask_app.config.mysqlconnections import connectToMySQL
from flask_app import DATABASE

# model the class after the ninjas table from our database
class Ninjas:
    def __init__( self , data:dict ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.age = data['age']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.dojo_id = data['dojo_id']
        #Add additional columns from database here


#CREATE
# create()
    @classmethod
    def create(cls, data:dict):
        query = "INSERT INTO ninjas (first_name, last_name, age, dojo_id) VALUES (%(first_name)s, %(last_name)s, %(age)s, %(dojo_id)s);"
        id = connectToMySQL(DATABASE).query_db(query, data)
        return id

#GET ALL
# get_all()
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls) -> list:
        """
        Explain What this function does
        This function gets all the ninjas from the database and
        reutnrs a list of INSTANCES!!. It doesn't recquire any
        parameters.
        """
        query = "SELECT * FROM ninjas;"

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
            

            #GET BY DOJO ID

    @classmethod
    def get_dojo(cls, data:dict):
        # query = "SELECT first_name, last_name, age FROM dojo_and_ninjas_schema.ninjas WHERE dojo_id = %(id)s;"
        query = "SELECT * FROM ninjas WHERE dojo_id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        ninjas = []
        for ninja in results:
            ninjas.append(cls(ninja))
        return ninjas
        # if not results:
        #     return []
        
        # dict = results[0]
        # instance = cls(dict)
        # return instance



#GET ONE
    @classmethod
    def get_one(cls, data:dict):
        """
        data dictionary needs a key of 'id'
        """
        query = "SELECT * FROM ninjas WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if not results:
            return []
        
        dict = results[0]
        instance = cls(dict)
        return instance
    
