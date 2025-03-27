from app import app
from app.db import init.db

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
    