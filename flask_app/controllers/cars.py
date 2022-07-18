from flask import redirect, request, render_template, session, flash
from flask_app.models import user, car
from flask_app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/process', methods = ['POST'])
def process():
    if request.form['type'] == 'register':
        if not user.User.validate_register(request.form):
            return redirect('/')
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password':bcrypt.generate_password_hash(request.form['password']) 
        }
        print('a punto de guardar')
        session['id'] = user.User.save(data)
        return redirect('/dashboard')

    elif request.form['type'] == 'login':
        user1 = user.User.get_user_by_email(request.form['email']) 
        if user1 == False or not bcrypt.check_password_hash(user1.password, request.form['password']):
            flash('Invalid email/password', category = 'login')
            return redirect('/')
        session['id'] = user1.id
        return redirect('/dashboard')
    elif request.form['type'] == 'new_car':
        if not car.Car.validate_car(request.form):
            return redirect('/new')
        data = {
            'price': request.form['price'],
            'model': request.form['model'],
            'make': request.form['make'],
            'year': request.form['year'],
            'description': request.form['description'],
            'seller_id': request.form['seller_id']
        }
        id = car.Car.save(data)   
        return redirect('/dashboard')
        # return redirect(f'/show/{id}')
    elif request.form['type'] == 'edit_car':
        if not car.Car.validate_car(request.form):
            return redirect(f'/edit/{request.form["car_id"]}')
        data = {
            'car_id': request.form['car_id'],
            'price': request.form['price'],
            'model': request.form['model'],
            'make': request.form['make'],
            'year': request.form['year'],
            'description': request.form['description']
        }
        car.Car.update(data)
        return redirect('/dashboard') 
        # return redirect(f'/show/{request.form["car_id"]}') 

@app.route('/dashboard')
def cars():
    if not 'id' in session:
        return redirect('/')
    user1 = user.User.get_user_by_id(session['id'])
    cars = car.Car.get_all()
    return render_template('cars.html', user = user1, cars = cars)

@app.route('/new')
def new():
    if not 'id' in session:
        return redirect('/')
    user1 = user.User.get_user_by_id(session['id'])
    return render_template('new_car.html', user = user1)

@app.route('/edit/<int:id>')
def edit(id):
    if not 'id' in session:
        return redirect('/')
    user1 = user.User.get_user_by_id(session['id'])
    car1 = car.Car.get_car_by_id_with_seller(id)
    if session['id'] != car1.seller_id:
        return redirect('/cars')
    return render_template('edit.html', user = user1, car = car1)

@app.route('/show/<int:id>')
def the_recipe(id):
    if not 'id' in session:
        return redirect('/')
    user1 = user.User.get_user_by_id(session['id'])
    car1 = car.Car.get_car_by_id_with_seller(id)
    return render_template('show.html', user = user1, car = car1)

@app.route('/purchase/<int:id>')
def purchase(id):
    if not 'id' in session:
        return redirect('/')
    car1 = car.Car.get_car_by_id(id)
    if int(session['id']) != int(car1.seller_id):
        data = {
            'car_id':id,
            'buyer_id':session['id']
        }
        car.Car.buy_car(data)
    return redirect('/dashboard')

@app.route('/user/<int:id>')
def my_cars(id):
    if not 'id' in session:
        return redirect('/')
    user1 = user.User.get_user_with_purchased_cars(session['id'])
    return render_template('owned.html', user = user1, cars = user1.cars)

@app.route('/delete/<int:id>')
def delete(id):
    if not 'id' in session:
        return redirect('/')
    car1 = car.Car.get_car_by_id(id)
    if int(session['id']) == int(car1.seller_id):
        car.Car.delete(id)
    return redirect('/dashboard')



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

