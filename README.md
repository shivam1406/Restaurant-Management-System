# 🍽️ Restaurant Management System
![Python](https://img.shields.io/badge/Python-3.9.12%2B-blue.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Contributions](https://img.shields.io/badge/Contributions-Welcome-blueviolet)
[![GitHub license](https://img.shields.io/github/license/shivam1406/Restaurant-Management-System)](https://github.com/shivam1406/Restaurant-Management-System/blob/master/LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/shivam1406/Restaurant-Management-System)](https://github.com/shivam1406/Restaurant-Management-System/commits/master)


A full-stack Flask-based web application to manage restaurant operations, including menu management, table reservations, order placement (admin + guest), and real-time order tracking.

![screenshot](screenshots/Dashboard.png)

---

## 🔧 Features


- 🔐 Role-based login (Admin/Guest)
- 📋 Add, edit, delete menu items
- 🪑 Manage restaurant tables
- 📦 Create and manage orders
- 🎫 Status tracking with badges (Pending, Preparing, Served, etc.)
- 👥 Public order form for guests
- 🧑‍💼 Admin dashboard with real-time updates
- 💡 Mobile-responsive and accessible design
- 🍽️ Order summary with grand total calculation

---

## 🛠 Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **Database:** MySQL
- **Templating:** Jinja2
- **Session Management:** Flask-Session
- **Other Tools:** Bootstrap, Git, GitHub

---

## 🚀 Getting Started

### 🔗 Clone the repository

```bash
git clone https://github.com/shivam1406/Restaurant-Management-System.git
cd Restaurant-Management-System
```

### 🧪 Setup virtual environment

```bash
python -m venv venv
# Activate on Windows:
venv\Scripts\activate
# Activate on macOS/Linux:
source venv/bin/activate
```

### 📦 Install dependencies

```bash
pip install -r requirements.txt
```

### ⚙️ Configure MySQL and Database

Create a MySQL database and configure your credentials in config.py or environment variables.

### 🔄 Initialize the database(Optional)

```bash
# If you have a route for seeding dummy data
http://localhost:5000/init/reset
```

### ▶️ Running the App

```bash
python app.py
```
Visit: http://127.0.0.1:5000

### 📁 Project Structure

```bash
RMS/
├── app.py
├── config.py
├── routes/
├── static/
│   └── css, js, images
├── templates/
│   └── *.html
├── utils/
│   └── db.py, auth.py
├── .gitignore
├── README.md
```

---

## 📸 Screenshots

### ✨ Dashboard
![Dashboard Screenshot](screenshots/Dashboard.png)

### ✨ Login
![Dashboard Screenshot](screenshots/Login.png)

### ✨ Logout
![Dashboard Screenshot](screenshots/Logout.png)

### ✨ Table  Management Page
![Dashboard Screenshot](screenshots/Table-management.png)

### ✨ Add Table
![Dashboard Screenshot](screenshots/Add-table.png)

### ✨ Edit Table
![Dashboard Screenshot](screenshots/Edit-table.png)

### ✨ Delete Table
![Dashboard Screenshot](screenshots/Delete-table.png)

### ✨ Menu Management Page
![Dashboard Screenshot](screenshots/Menu-management.png)

### ✨ Add Menu Item
![Dashboard Screenshot](screenshots/Add-menu-item.png)

### ✨ Edit Menu Item
![Dashboard Screenshot](screenshots/Edit-menu-item.png)

### ✨ Delete Menu Item
![Dashboard Screenshot](screenshots/Delete-menu-item.png)

### ✨ Order Management Page
![Dashboard Screenshot](screenshots/Order-management.png)

### ✨ Admin Add Order
![Dashboard Screenshot](screenshots/Admin-add-order.png)

### ✨ View Order Details
![Dashboard Screenshot](screenshots/View-order-details.png)

### ✨ Delete Order
![Dashboard Screenshot](screenshots/Delete-order.png)

### ✨ Self Order Page
![Public Order](screenshots/Self-order.png)

---

## 🤝 Contribute
Pull requests welcome! For major changes, open an issue first to discuss what you’d like to change.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).

---

## 🙋‍♂️ Author

**Shivam**  
📧 [ss.shivam1406@gmail.com](mailto:ss.shivam1406@gmail.com)  
🔗 [LinkedIn – ssshivam1406](https://www.linkedin.com/in/ssshivam1406/)