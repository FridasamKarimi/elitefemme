import psycopg2
from .config import DB_CONFIG

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                 id SERIAL PRIMARY KEY, 
                 name TEXT NOT NULL, 
                 price REAL NOT NULL, 
                 description TEXT, 
                 stock INTEGER NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
                 id SERIAL PRIMARY KEY, 
                 items TEXT NOT NULL, 
                 total REAL NOT NULL, 
                 status TEXT NOT NULL)''')
    c.execute("SELECT COUNT(*) FROM products")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO products (name, price, description, stock) VALUES (%s, %s, %s, %s)", 
                  ("Dera's Coconut Oil", 12.00, "Pure, natural coconut oil for skin and hair", 50))
        c.execute("INSERT INTO products (name, price, description, stock) VALUES (%s, %s, %s, %s)", 
                  ("Mabuyu", 5.00, "Tangy, sweet baobab candy treat", 100))
    conn.commit()
    conn.close()