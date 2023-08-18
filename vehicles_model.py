from flask_app.config.mysqlconnection import connectToMySQL
import pprint, re
from flask_app.models import members_model
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask import flash


class Vehicle:
    db ="americancarclub"
    def __init__(self,data):
        self.id = data['id']
        self.mileage = data['mileage']
        self.make = data['make']
        self.model = data['model']
        self.year = data['year']
        self.modifications = data['modifications']
        self.image = data['image']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.member_id = data['member_id']
        self.owner = None


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM vehicles;"
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        vehicles = []
        for r in results:
            vehicles.append( cls(r))
        return vehicles
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO vehicles (mileage, make, model, year, modifications, image, member_id) VALUES (%(mileage)s, %(make)s, %(model)s, %(year)s, %(modifications)s, %(image)s, %(member_id)s);"
        result = connectToMySQL(cls.db).query_db(query,data)
        return result
    

    @classmethod
    def update(cls,data):
        query = "UPDATE vehicles SET mileage = %(mileage)s, make = %(make)s, model = %(model)s, year = %(year)s, modifications = %(modifications)s, member_id = %(member_id)s WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        return result
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT *  FROM cars WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])
    
    #@classmethod
    #def get_one(cls,data):
    #    query = "SELECT *  FROM cars WHERE id = %(id)s;"
    #    results = connectToMySQL(cls.db).query_db(query,data)
    #    return cls(results[0])

    @classmethod
    def get_one_vehicle_w_member(cls, data):
        query = "SELECT * FROM vehicles LEFT JOIN members ON vehicles.member_id = members.id WHERE vehicles.id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query,data)
        single_vehicle = cls(results[0])

        for row in results:
            member_data = {
                "id": row["members.id"],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at']
            }

        single_vehicle.owner = members_model.Member(member_data)
        print('single_vehicle', single_vehicle)
        return single_vehicle

    @classmethod
    def get_all_w_members(cls): 
        query = "SELECT * FROM vehicles LEFT JOIN members ON vehicles.member_id = members.id;" 
        result = connectToMySQL(cls.db).query_db(query)
        print(result)
        vehicles = []  #
        for row in result: 
            print(row)
            new_vehicle = cls(row) 
            member_data = {
                "id": row["members.id"],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": '',
                "created_at": row['members.created_at'], #we are prefixing to specify which table we are pullin from.
                "updated_at": row['members.updated_at']
            }
            new_vehicle.owner = members_model.Member(member_data) 
            vehicles.append(new_vehicle)
        return vehicles


    @classmethod
    def delete(cls, data):
        
        query  = "DELETE FROM vehicles WHERE id = %(id)s"
        
        result = connectToMySQL(cls.db).query_db(query, data)
        print("result", result)
        return result   
    
    @staticmethod
    def validate_vehicle(vehicle):
        is_valid = True
        #query = "SELECT * FROM vehicles WHERE email = %(email)s;"
        #results = connectToMySQL("americancarclub").query_db(query,vehicle)
            
        if len(vehicle['model']) < 3:
            flash("model field cannot be left empty","vehicle")
            is_valid = False
        if len(vehicle['make']) < 0:
            flash("make field cannot be empty","vehicle")
            is_valid = False
        if len(vehicle['year']) < 0:
            flash("Year must be higher than 0!!!!","vehicle")
        if len(vehicle['modifications']) < 0:
            flash("Modification field cannot be empty!!!!","vehicle")
            is_valid = False

        return(is_valid)