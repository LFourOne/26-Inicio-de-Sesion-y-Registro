from app_flask.config.mysqlconnections import connectToMySQL
from flask import flash
from app_flask import DATA_BASE, EMAIL_REGEX

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.password = data['password']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    
    @classmethod
    def create_one(cls, data):
        query = """
                INSERT INTO users(first_name, last_name, password, email)
                VALUE (%(first_name)s, %(last_name)s, %(password)s, %(email)s);
                """
        return connectToMySQL(DATA_BASE).query_db(query, data)  
    
    @classmethod
    def obtain_one(cls, data):
        query = """
                SELECT *
                FROM users
                WHERE email = %(email)s;
                """
        result = connectToMySQL(DATA_BASE).query_db(query, data)
        if len(result) == 0:
            return None
        return cls(result[0])
    
    
    @staticmethod
    def validate_register(data):
        is_valid = True
        if len(data['first_name']) < 2:
            is_valid = False
            flash('Please, enter your name', 'first_name_error')
        if len(data['last_name']) < 2:
            is_valid = False
            flash('Please, enter your last name', 'last_name_error')
        if not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash('Please, enter a valid email', 'email_error')
        if data['password'] != data['password_confirm']:
            is_valid = False
            flash('Your passwords, doesnt match!', 'password_error')
        if len(data['password']) < 8:
            is_valid = False
            flash('Your password must be a minimum of 8 characters', 'password_error')
        return is_valid