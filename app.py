from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    return sqlite3.connect("database.db")

def init_db():
    """Initialize database with tables if they don't exist"""
    conn = get_db()
    c = conn.cursor()
    
    # Users Table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'user'
    )''')
    
    # Meals Table
    c.execute('''CREATE TABLE IF NOT EXISTS meals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        meal_name TEXT NOT NULL,
        price REAL NOT NULL
    )''')
    
    # Orders Table
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        meal_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(meal_id) REFERENCES meals(id)
    )''')
    
    # Create default admin user if it doesn't exist
    c.execute("SELECT * FROM users WHERE email=?", ("admin@tiffin.com",))
    admin = c.fetchone()
    if not admin:
        c.execute("INSERT INTO users(name,email,password,role) VALUES (?,?,?,?)",
                  ("Admin", "admin@tiffin.com", "admin123", "admin"))
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        try:
            conn = get_db()
            c = conn.cursor()
            c.execute("INSERT INTO users(name,email,password) VALUES (?,?,?)", (name,email,password))
            conn.commit()
            conn.close()
            flash("Registration successful! Please login.", "success")
            return redirect("/login")
        except sqlite3.IntegrityError:
            flash("Email already exists! Please use a different email.", "error")
        except Exception as e:
            flash("Registration failed. Please try again.", "error")
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password=?", (email,password))
        user = c.fetchone()
        conn.close()

        if user:
            session["user_id"] = user[0]
            session["user_name"] = user[1]
            session["role"] = user[4]
            flash(f"Welcome back, {user[1]}!", "success")
            if user[4] == "admin":
                return redirect("/admin")
            return redirect("/user")
        else:
            flash("Invalid email or password!", "error")

    return render_template("login.html")

@app.route("/user")
def user_dashboard():
    if "user_id" not in session:
        return redirect("/login")
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM meals")
    meals = c.fetchall()
    conn.close()
    return render_template("dashborad_user.html", meals=meals)


@app.route("/admin")
def admin_dashboard():
    if "role" not in session or session["role"] != "admin":
        return redirect("/login")
    return render_template("dashboard_admin.html")

@app.route("/meals", methods=["GET","POST"])
def meals():
    if "role" not in session or session["role"] != "admin":
        return redirect("/login")

    conn = get_db()
    c = conn.cursor()

    if request.method == "POST":
        meal_name = request.form["meal_name"]
        price = request.form["price"]
        try:
            c.execute("INSERT INTO meals(meal_name,price) VALUES(?,?)", (meal_name, price))
            conn.commit()
            flash("Meal added successfully!", "success")
        except Exception as e:
            flash("Failed to add meal. Please try again.", "error")

    c.execute("SELECT * FROM meals ORDER BY id DESC")
    meals = c.fetchall()
    conn.close()

    return render_template("meals.html", meals=meals)

@app.route("/order/<int:meal_id>")
def order(meal_id):
    if "user_id" not in session:
        return redirect("/login")

    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("INSERT INTO orders(user_id, meal_id, date) VALUES(?,?,?)",
                  (session["user_id"], meal_id, datetime.now().strftime("%Y-%m-%d")))
        conn.commit()
        conn.close()
        flash("Order placed successfully!", "success")
    except Exception as e:
        flash("Failed to place order. Please try again.", "error")

    return redirect("/user")

@app.route("/orders")
def view_orders():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    c = conn.cursor()
    
    # Admin can see all orders, users see only their orders
    if session.get("role") == "admin":
        c.execute("""SELECT orders.id, meals.meal_name, meals.price, orders.date, users.name as user_name
                     FROM orders 
                     JOIN meals ON orders.meal_id = meals.id
                     JOIN users ON orders.user_id = users.id
                     ORDER BY orders.date DESC, 
                     orders.id DESC""")
    else:
        c.execute("""SELECT orders.id, meals.meal_name, meals.price, orders.date
                     FROM orders JOIN meals ON orders.meal_id = meals.id
                     WHERE user_id=?
                     ORDER BY orders.date DESC, orders.id DESC""", (session["user_id"],))
    
    orders = c.fetchall()
    conn.close()

    return render_template("orders.html", orders=orders)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
