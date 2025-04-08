import psycopg2
from .config import Config

def get_db_connection():
    conn = psycopg2.connect(
        dbname=Config.DB_CONFIG['elitefemmedb'],
        user=Config.DB_CONFIG['frida'],
        password=Config.DB_CONFIG['root'],
        host=Config.DB_CONFIG['host'],
        port=Config.DB_CONFIG['5432']
    )
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Create products table
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            description TEXT,
            stock INT NOT NULL
        )
    ''')
    # Create orders table (updated)
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(user_id),
            total DECIMAL(10, 2) NOT NULL,
            status VARCHAR(20) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Create order_items table
    c.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id SERIAL PRIMARY KEY,
            order_id INTEGER REFERENCES orders(order_id),
            product_id INTEGER REFERENCES products(product_id),
            quantity INTEGER NOT NULL,
            price_at_time DECIMAL(10, 2) NOT NULL
        )
    ''')
    # Insert sample data if tables are empty
    c.execute("SELECT COUNT(*) FROM products")
    if c.fetchone()[0] == 0:
        c.execute("""
            INSERT INTO products (name, price, description, stock) VALUES
            ('Natural Lip Balm', 5.99, 'Organic lip care', 100),
            ('Elite Moisturizer', 19.99, 'Hydrates all day', 50)
        """)
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        # Sample user (password: "test123" hashed)
        c.execute("""
            INSERT INTO users (username, email, password_hash) VALUES
            ('testuser', 'test@example.com', '$2b$12$K.ixk1Z6e3e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e')
        """)
    conn.commit()
    conn.close()