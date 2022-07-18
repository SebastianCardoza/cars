from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import car
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.cars = []

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) values (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        return connectToMySQL('esquema_carros').query_db(query,data)

    @classmethod
    def get_user_by_id(cls, id):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        data = {'id':id}
        results = connectToMySQL('esquema_carros').query_db(query, data)
        user = cls(results[0])
        return user

    @classmethod
    def get_user_by_email(cls, email):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        data = {'email': email}
        print('se logro?')
        results = connectToMySQL('esquema_carros').query_db(query, data)
        if len(results) > 0:
            return cls(results[0])
        return False

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL('esquema_carros').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def delete(cls, id):
        query = 'DELETE FROM users WHERE id = %(id)s;'
        data = {'id': id}
        connectToMySQL('esquema_carros').query_db(query, data)

    @classmethod
    def get_user_with_purchased_cars(cls, id):
        query = 'SELECT * FROM users LEFT JOIN cars ON users.id = cars.buyer_id WHERE users.id = %(id)s;'
        data = {'id':id}
        results = connectToMySQL('esquema_carros').query_db(query, data)
        user = cls(results[0])
        for row_in_db in results:
            data = {
                'id':row_in_db['cars.id'],
                'price':row_in_db['price'],
                'model':row_in_db['model'],
                'make':row_in_db['make'],
                'year':row_in_db['year'],
                'description':row_in_db['description'],
                'seller_id':row_in_db['seller_id'],
                'buyer_id':row_in_db['buyer_id'],
                'created_at':row_in_db['cars.created_at'],
                'updated_at':row_in_db['cars.updated_at']
            }
            user.cars.append(car.Car(data))
        return user


    @staticmethod
    def validate_register(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash('First name has to be at least 2 characters', category='register')
            is_valid = False
        if len(user['last_name']) < 2:
            flash('Last name has to be at least 2 characters', category='register')
            is_valid = False
        if User.get_user_by_email(user['email']) != False:
            flash('Email already exists', category='register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Email is not valid', category='register')    
            is_valid = False
        if len(user['password']) < 8:
            flash('Password has to be at least 8 characters', category='register')
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash('Passwords doesnt match', category='register')
            is_valid = False
        return is_valid
