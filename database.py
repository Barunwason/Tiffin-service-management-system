import sqlite3

def create_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Users Table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT DEFAULT 'user'
    )''')

    # Meals Table
    c.execute('''CREATE TABLE IF NOT EXISTS meals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        meal_name TEXT,
        price INTEGER
    )''')

    # Orders Table
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        meal_id INTEGER,
        date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(meal_id) REFERENCES meals(id)
    )''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
