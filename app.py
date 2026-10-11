from flask import Flask, render_template, request, redirect, url_for, session
import datetime
from database import init_db, verify_user, register_user, fetch_menu, add_menu_item, save_order, fetch_orders, update_order_status

app = Flask(__name__)
app.secret_key = "restoflow_secret_key_pbl"

# Force initialize database and tables on startup
init_db()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = verify_user(username, password)
        if user:
            session["username"] = user[0]
            session["role"] = user[1]
            return redirect(url_for("pos"))
        else:
            return render_template("login.html", error="Invalid Username or Password")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        
        success = register_user(username, password, role)
        if success:
            return redirect(url_for("login"))
        else:
            return render_template("register.html", error="Username already taken. Choose another.")
            
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/pos", methods=["GET", "POST"])
def pos():
    if "username" not in session:
        return redirect(url_for("login"))
    
    menu_items = fetch_menu()
    
    if request.method == "POST":
        table_no = request.form.get("table_no")
        customer_name = request.form.get("customer_name")
        
        subtotal = 0
        order_details_text = ""
        
        for item in menu_items:
            item_id = str(item[0])
            qty_str = request.form.get(f"qty_{item_id}")
            if qty_str and int(qty_str) > 0:
                qty = int(qty_str)
                price = item[3]
                cost = qty * price
                subtotal += cost
                order_details_text += f"{item[1]} x{qty} (${cost:.2f}), "
        
        if subtotal > 0:
            tax = subtotal * 0.05
            total = subtotal + tax
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            save_order(table_no, order_details_text.strip(", "), total, "Preparing", current_time, session["username"])
            return render_template("pos.html", menu_items=menu_items, success="Order placed successfully!")
            
    return render_template("pos.html", menu_items=menu_items)

@app.route("/kitchen", methods=["GET", "POST"])
def kitchen():
    if "username" not in session:
        return redirect(url_for("login"))
        
    if request.method == "POST":
        order_id = request.form.get("order_id")
        new_status = request.form.get("status")
        update_order_status(order_id, new_status)
        return redirect(url_for("kitchen"))
        
    orders = fetch_orders()
    return render_template("kitchen.html", orders=orders)

@app.route("/menu", methods=["GET", "POST"])
def menu_mgmt():
    if "username" not in session or session.get("role") != "Admin":
        return redirect(url_for("pos"))
        
    if request.method == "POST":
        name = request.form.get("name")
        category = request.form.get("category")
        price = float(request.form.get("price"))
        stock = int(request.form.get("stock"))
        add_menu_item(name, category, price, stock)
        return redirect(url_for("menu_mgmt"))
        
    menu_items = fetch_menu()
    return render_template("menu.html", menu_items=menu_items)

@app.route("/analytics")
def analytics():
    if "username" not in session or session.get("role") != "Admin":
        return redirect(url_for("pos"))
    orders = fetch_orders()
    total_revenue = sum([o[3] for o in orders]) if orders else 0
    total_orders = len(orders)
    return render_template("analytics.html", total_revenue=total_revenue, total_orders=total_orders)

if __name__ == "__main__":
    app.run(debug=True)