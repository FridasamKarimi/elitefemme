from flask import render_template, request, jsonify, redirect, url_for
from . import app
from .db import get_db_conection
import stripe 
from .config import Config

stripe.api_key = Config.STRIPE_SECRET_KEY

@app.route('/')
def home():
    conn = get_db_conection()
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
    return render_template('contact.html', success=request.args.get('success', False))
total = sum(item['price'] for item in cart)
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    cart = request.json['cart']
    conn = get_db_conection()
    c = conn.cursor()
    items = ', '.join([f"{item['name']} (${item['price']})" for item in cart])

    c.execute("INSERT INTO orders (items, total, status) VALUES (%s, %s, %s) RETURNING id", 
              (items, total, 'pending'))
    order_id = c.fetchone()[0]
    conn.commit()
    conn.close()
    line_items = [{'price_data': {'currency': 'usd', 'product_data': {'name': item['name']}, 
                                  'unit_amount': int(item['price'] * 100)}, 'quantity': 1} 
                  for item in cart]
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url='http://localhost:5000/success?order_id=' + str(order_id),
        cancel_url='http://localhost:5000/cancel'
    )
    return jsonify({'id': session.id})

@app.route('succes')
def success():
    order_id = request.args.get('orders_id')
    conn = get_db_conection()
    c = conn.cursor()
    c.execute("UPDATE orders SET status = %s", ('completed', order_id))
    conn.commit()
    conn.close()
    return "Payment Successful! Thankyou you for shopping with EliteFemme."

@app.route('/cancel')
def cancel():
    return "Payment canceled. Back to shopping?"

    