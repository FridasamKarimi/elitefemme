from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_login import login_user, logout_user, login_required, current_user  # Add login_required here
from werkzeug.security import generate_password_hash, check_password_hash
from . import app
from .db import get_db_connection
from .models import User

@app.route('/')
def home():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = [{'id': row[0], 'name': row[1], 'price': row[2], 'description': row[3], 'stock': row[4]}
                for row in c.fetchall()]
    conn.close()
    return render_template('index.html', products=products)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        print(f"Contact Form: {name}, {email}, {message}")
        return redirect(url_for('contact', success=True))
    return render_template('contact.html', succes=request.args.get('success', False))
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.find_by_email(email)
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('home'))
        flash('invalid email or passowrd')
        return render_template('login.html')
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.find_by_email(email):
            flash('Email already registered')
        else:
            password_hash = generate_password_hash(password)
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("INSERT INTO users (username, email, pasword_harsh) VALUES (%s, %s, %s)",
                        (username, email, password_hash))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        return render_template('register.html')  

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart = request.json.get('cart', [])
    if not cart:
        return jsonify({'error': 'Cart is empty'}), 400
    total = sum(item['price'] for item in cart)
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO orders (user_id, total, status) VALUES (%s, %s, %s) RETURNING order_id",
              (current_user.id, total, 'completed'))
    order_id = c.fetchone()[0]
    for item in cart:
        c.execute("INSERT INTO order_items (order_id, product_id, quantity, price_at_time) VALUES (%s, %s, %s, %s)",
                  (order_id, item['id'], 1, item['price']))  #
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'order_id': order_id})

@app.route('/success')
def success():
    order_id = request.args.get('order_id')
    return f"Order #{order_id} Successful! Thank you for shopping with EliteFemme."

@app.route('/cancel')
def cancel():
    return "Checkout canceled. Back to shopping?"



        

        
