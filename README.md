
# 🍽️ Restaurant Management System
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Framework-Flask-black)
![SQLite](https://img.shields.io/badge/Database-SQLite-blue)
![Status](https://img.shields.io/badge/Status-Live-success)

A web-based **Restaurant Management System** built using Python Flask and SQLite to simplify restaurant operations, manage orders, maintain menu items, and monitor restaurant performance through an analytics dashboard.

## 🚀 Features

### 🔐 User Authentication
- Secure login and registration.
- Role-based access for Admin and Staff.
- Session-based authentication.
- Logout functionality.

### 🛒 Point of Sale (POS)
- Create customer orders.
- Assign orders to specific tables.
- Select menu items and quantities.
- Automatic subtotal and 5% tax calculation.
- Save orders to the database.

### 📋 Menu Management
- Add new food items.
- Manage item names and categories.
- Set prices and stock quantities.
- Admin-only menu management.

### 👨‍🍳 Kitchen Management
- View incoming restaurant orders.
- Monitor order details.
- Update order preparation status.
- Track order progress.

### 📊 Analytics Dashboard
- View total orders.
- Calculate total restaurant revenue.
- Monitor overall order performance.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web framework |
| SQLite | Database management |
| HTML5 | Frontend structure |
| CSS3 | Styling |
| Jinja2 | Dynamic HTML templates |

## 📁 Project Structure

```text
restuarant-management/
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── pos.html
│   ├── kitchen.html
│   ├── menu.html
│   └── analytics.html
│
├── app.py
├── database.py
├── restaurant.db
└── README.md
```

## ⚙️ Installation & Setup

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/hassannn434/restuarant-management.git
```

### 2. Navigate to the Project Directory

```bash
cd restuarant-management
```

### 3. Install Required Dependencies

```bash
pip install flask
```

### 4. Run the Application

```bash
python app.py
```

### 5. Open in Browser

Visit:

```text
http://127.0.0.1:5000/
```

The SQLite database and required tables are initialized automatically when the application starts.

## 🔑 Default Login Credentials

The application initializes the following default accounts when the users table is empty.

| Role | Username | Password |
|---|---|---|
| Admin | admin | admin123 |
| Staff | waiter1 | waiter123 |

**Note:** Change the default credentials before using the application in a real environment.

## 🗄️ Database Structure

The application uses SQLite with the following main tables:

- **Users:** Stores usernames, password hashes and user roles.
- **Menu:** Stores food item names, categories, prices and stock.
- **Orders:** Stores table numbers, order details, totals, preparation status and staff information.

  ## 🌐 Live Demo

Experience the Restaurant Management System:

🔗 **Live Application:** https://hassanmahadkar.pythonanywhere.com/

### Demo Credentials

| Role | Username | Password |
|---|---|---|
| Admin | admin | admin123 |
| Staff | waiter1 | waiter123 |

## 🔮 Future Enhancements

- Online food ordering and reservations.
- Payment gateway integration.
- Advanced sales and revenue reports.
- Inventory alerts and stock management.
- Customer feedback and ratings.
- Responsive mobile-friendly interface.

## 👨‍💻 Author

**Hassan Mahadkar**

GitHub: [@hassannn434](https://github.com/hassannn434)

Project Repository: [Restaurant Management System](https://github.com/hassannn434/restuarant-management)

---

⭐ If you find this project useful, consider giving it a star!

**Built with Python, Flask and SQLite.**
