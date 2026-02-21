# 🎓 Attendance Management System (Python + MySQL)

A simple Attendance Management System built using Python and MySQL.

---

## 📌 Features

- Add / Remove / Update Students
- Mark Attendance
- View Attendance by Date
- View Attendance by Student
- Modify Attendance
- Export Attendance to CSV

---

## 🛠 Technologies Used

- Python
- MySQL
- mysql-connector-python
- tabulate

---

## ⚙️ Installation & Setup (For Beginners)

### 1️⃣ Install Python
Download from:
https://www.python.org/downloads/

---

### 2️⃣ Install MySQL
Download MySQL Server and MySQL Command Line Client.

---

### 3️⃣ Install Required Libraries

Open terminal inside project folder and run:

pip install -r requirements.txt

---

### 4️⃣ Setup Database in MySQL

Open **MySQL Command Line Client** and run:


**CREATE DATABASE STUDENT;
USE STUDENT;**

**CREATE TABLE students (
rollno INT PRIMARY KEY,
student_name VARCHAR(50)
);**

CREATE TABLE attendance (
rollno INT,
attendance_date DATE,
status VARCHAR(20),
FOREIGN KEY (rollno) REFERENCES students(rollno)
);
---

### 5️⃣ Update MySQL Password in Code

Open `student_attendence.py` and change:

password="your_mysql_password"

---

### 6️⃣ Run The Project

python student_attendence.py

---

## 👨‍💻 Author

**Manish Debnath**

First Year Student | Beginner Python Developer
