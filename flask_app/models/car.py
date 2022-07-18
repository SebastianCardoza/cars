from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Car:
    def __init__(self, data):
        self.id = data['id']
        self.price = data['price']
        self.model = data['model']
        self.make = data['make']
        self.year = data['year']
        self.description = data['description']
        self.seller_id = data['seller_id']
        self.buyer_id = data['buyer_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.seller = None

    @classmethod
    def save(cls, data):
        data['seller_id'] = int(data['seller_id'])
        query = 'INSERT INTO cars (price, model, make, year, description, seller_id) values (%(price)s, %(model)s, %(make)s, %(year)s, %(description)s, %(seller_id)s);'
        return connectToMySQL('esquema_carros').query_db(query,data)

    @classmethod
    def get_car_by_id(cls, id):
        query = 'SELECT * FROM cars WHERE id = %(id)s;'
        data = {'id':id}
        results = connectToMySQL('esquema_carros').query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_car_by_id_with_seller(cls, id):
        query = 'SELECT * FROM cars WHERE id = %(id)s;'
        data = {'id':id}
        results = connectToMySQL('esquema_carros').query_db(query, data)
        car = cls(results[0])
        car.seller = user.User.get_user_by_id(car.seller_id)
        return car

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM cars;'
        results = connectToMySQL('esquema_carros').query_db(query)
        cars = []
        for car in results:
            car = cls(car)
            car.seller = user.User.get_user_by_id(car.seller_id)
            cars.append(car)
        return cars

    @classmethod
    def delete(cls, id):
        query = 'DELETE FROM cars WHERE id = %(id)s;'
        data = {'id': id}
        connectToMySQL('esquema_carros').query_db(query, data)

    @classmethod
    def update(cls, data):
        query = 'UPDATE cars SET price = %(price)s, model = %(model)s, make = %(make)s, year = %(year)s, description = %(description)s WHERE id = %(car_id)s;'    
        connectToMySQL('esquema_carros').query_db(query, data)

    @classmethod
    def buy_car(cls, data):
        query = 'UPDATE cars SET buyer_id = %(buyer_id)s WHERE id = %(car_id)s;'    
        connectToMySQL('esquema_carros').query_db(query, data)

    @staticmethod
    def validate_car(car):
        is_valid = True
        if len(car['model']) < 1:
            flash('Model is required', category='new_car')
            is_valid = False
        if len(car['description']) < 3:
            flash('Description has to be at least 3 characters', category='new_car')
            is_valid = False
        if len(car['make']) < 1:
            flash('Make is required', category='new_car')
            is_valid = False
        if int(car['year']) < 1000:
            flash('Year has to has 4 digits', category='new_car')
            is_valid = False
        if int(car['price']) < 1:
            flash('Price has to be greater than 0', category='new_car')
            is_valid = False
        return is_valid
