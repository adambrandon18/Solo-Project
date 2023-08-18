from flask_app.config.mysqlconnection import connectToMySQL
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
#THE CODE ABOVE HAS A METHOD REFERRED TO AS MATCH THAT WILL RETURN NONE IF THEIR IS NO MATCH LOCATED
from flask import flash

class Member:
    db ="americancarclub"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        #self.member_id = data['member_id']
        



    @classmethod
    def save(cls, data):   
        query = "INSERT INTO  members(first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s, %(email)s, %(password)s);"
        result = connectToMySQL(cls.db).query_db(query,data) 
        return result
    


    @staticmethod
    def validate_register(data):
        is_valid = True
        query = "SELECT * FROM members WHERE email = %(email)s;"
        results = connectToMySQL("AmericanCarClub").query_db(query,data)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email!!!","register")
            is_valid = False
        if len(data['first_name']) < 3:
            flash("First name must be at least 3 characters","register")
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Last name must be at least 3 characters","register")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid = False
        if data['password']  != data['comfirm']:
            flash("Please make sure your passwords match!! ","register")
            is_valid = False
        return is_valid
    

    
    @classmethod
    def get_by_id(cls,data):   
        query = "SELECT * FROM members WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        #print('results', results)
        #print("a", data)
        return cls(results[0])
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM members WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        if len(results) < 1:
            print(results)
            return False
        return cls(results[0])
    
    
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM members;"
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        members = []
        for u in results:
            members.append( cls(u) )
        return members