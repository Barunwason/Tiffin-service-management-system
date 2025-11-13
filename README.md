# Tiffin Management System

A modern, responsive web application for managing tiffin meal orders and deliveries.

## Features

- ✅ User Registration and Login
- ✅ Admin Dashboard for managing meals
- ✅ User Dashboard for browsing and ordering meals
- ✅ Order Management System
- ✅ Responsive Design (works on mobile, tablet, and desktop)
- ✅ Modern UI with beautiful styling
- ✅ Flash messages for user feedback
- ✅ Database initialization on startup

## Setup Instructions

1. **Activate Virtual Environment:**
   ```bash
   my_env\Scripts\activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install flask
   ```

3. **Run the Application:**
   ```bash
   python app.py
   ```

4. **Access the Application:**
   - Open your browser and go to: `http://127.0.0.1:5000`

## Default Admin Credentials

- **Email:** admin@tiffin.com
- **Password:** admin123

## Usage

### For Users:
1. Register a new account or login
2. Browse available meals on the dashboard
3. Click "Order Now" to place an order
4. View your orders in "My Orders"

### For Admins:
1. Login with admin credentials
2. Go to "Manage Meals" to add new meals
3. View all customer orders in "View All Orders"
4. Manage the menu and track orders

## Database

The database (`database.db`) is automatically created and initialized when the app starts. It includes:
- **users** table: Stores user information and roles
- **meals** table: Stores meal information and prices
- **orders** table: Stores order details

## Technology Stack

- **Backend:** Flask (Python)
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **Styling:** Custom CSS with responsive design

## Project Structure

```
.
├── app.py                 # Main Flask application
├── database.py            # Database initialization script
├── static/
│   └── style.css         # Stylesheet
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── dashborad_user.html  # User dashboard
│   ├── dashboard_admin.html # Admin dashboard
│   ├── meals.html        # Manage meals (admin)
│   └── orders.html       # View orders
└── database.db           # SQLite database (created automatically)
```

## Notes

- The application uses session-based authentication
- Passwords are stored in plain text (for development only - use hashing in production)
- The database is automatically initialized on startup
- All templates are responsive and work on mobile devices

