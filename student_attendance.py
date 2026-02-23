import mysql.connector as sql                           #connecting python to mysql
from tabulate import tabulate as tb                     #used for just printing the tables in a nice format
import csv                                              #Create a csv file for exporting

# ---------------- DATABASE FUNCTIONS ---------------- #

def execute_query(query, values=None):                  #creating a function that will run insert,update,delete queries 
    connection = sql.connect(                           #connecting our mysql with this program file
        host="localhost",
        database="STUDENT",
        user="root",
        password="password"
    )
    cursor = connection.cursor()                         #bringing the cursor to the terminal or on the sql page
    if values is not None:
        cursor.execute(query, values)                    #write the command in mysql
    else:
        cursor.execute(query)
    connection.commit()                                  #pressing enter in mysql shell
    cursor.close()                                       #closing everything
    connection.close()


def fetch_all(query, values=None):                       #Fetching data from the database
    connection = sql.connect(                                                   
        host="localhost",
        database="STUDENT",
        user="root",
        password="password"
    )
    cursor = connection.cursor()
    if values is not None:
        cursor.execute(query, values)
    else:
        cursor.execute(query)
    results = cursor.fetchall()                          #return the list of tuples
    cursor.close()
    connection.close()
    return results


# ---------------- MAIN MENU ---------------- #

def menu():                                              #function for menu
    print("=" * 40)
    print("------------------------------------------------------")
    print("------------ Attendance Management System ------------")
    print("------------------------------------------------------")
    print("1. Manage Students (Add/Remove/Update)")
    print("2. Mark Attendance")
    print("3. View Attendance Report")
    print("4. Modify Attendance")
    print("5. Export Attendance Report")
    print("6. Exit")
    print("=" * 40)
    return input("Enter your choice: ")


# ---------------- MANAGE STUDENTS ---------------- #

def manage_student():                                     #Student managemnet options
    print("------------------------------------------------------")
    print("------------------ Manage Students ------------------")
    print("------------------------------------------------------")
    print("1. Add Student")
    print("2. Remove Student")
    print("3. Update Student")
    print("4. View All Students")
    print("5. Exit")
    print("-------------------------------------------------------")

    choice = input("Enter your choice: ")

    if choice == "1":
        sid = int(input("Enter Roll No: "))
        name = input("Enter Name: ")
        query = "INSERT INTO students VALUES (%s, %s)"
        execute_query(query, (sid, name))
        print("*******************************************************")
        print("*************Student added successfully!***************")
        print("*******************************************************")

    elif choice == "2":
        sid = int(input("Enter Roll No to remove: "))
        query = "DELETE FROM students WHERE rollno = %s"
        execute_query(query, (sid,))
        print("*******************************************************")
        print("*************Student removed successfully!*************")
        print("*******************************************************")

    elif choice == "3":
        sid = int(input("Enter Roll No to update: "))
        name = input("Enter new Name: ")
        query = "UPDATE students SET student_name = %s WHERE rollno = %s"
        execute_query(query, (name, sid))
        print("********************************************************")
        print("*************Student updated successfully!*************")
        print("********************************************************")

    elif choice == "4":
        query = "SELECT * FROM students"
        data = fetch_all(query)
        headers = ["Roll No", "Name"]
        if data:
            print(tb(data, headers=headers, tablefmt="grid"))
        else:
            print("****************************************************")
            print("No students found.")
            print("****************************************************")


# ---------------- MARK ATTENDANCE ---------------- #

def mark_attendance():
    print("\n1. Mark Today's Attendance")
    print("2. Mark Attendance for Specific Date")
    choice = input("Enter your choice: ")

    if choice == "1":
        query = "SELECT rollno, student_name FROM students"
        students = fetch_all(query)

        for roll, name in students:
            status = input(f"{name} (Roll {roll}) [P/A]: ").upper()
            status = "Present" if status == "P" else "Absent"

            query = """
            INSERT INTO attendance (rollno, attendance_date, status)
            VALUES (%s, CURDATE(), %s)
            """
            execute_query(query, (roll, status))

        print("Attendance marked successfully!")

    elif choice == "2":
        date = input("Enter Date (YYYY-MM-DD): ")
        query = "SELECT rollno, student_name FROM students"
        students = fetch_all(query)

        for roll, name in students:
            status = input(f"{name} (Roll {roll}) [P/A]: ").upper()
            status = "Present" if status == "P" else "Absent"

            query = """
            INSERT INTO attendance (rollno, attendance_date, status)
            VALUES (%s, %s, %s)
            """
            execute_query(query, (roll, date, status))

        print("Attendance marked successfully!")


# ---------------- VIEW REPORT ---------------- #

def view_report():
    print("\n1. View by Date")
    print("2. View by Student")
    choice = input("Enter choice: ")

    if choice == "1":
        date = input("Enter Date (YYYY-MM-DD): ")
        query = """
        SELECT students.rollno, students.student_name, attendance.status
        FROM students
        JOIN attendance ON students.rollno = attendance.rollno
        WHERE attendance.attendance_date = %s
        """
        data = fetch_all(query, (date,))
        headers = ["Roll No", "Name", "Status"]
        if data:
            print(tb(data, headers=headers, tablefmt="grid"))
        else:
            print("No attendance found for this date.")

    elif choice == "2":
        roll = int(input("Enter Roll No: "))
        query = """
        SELECT attendance_date, status
        FROM attendance
        WHERE rollno = %s
        """
        data = fetch_all(query, (roll,))
        headers = ["Date", "Status"]
        if data:
            print(tb(data, headers=headers, tablefmt="grid"))
        else:
            print("No attendance found for this student.")


# ---------------- MODIFY ATTENDANCE ---------------- #

def modify_attendance():
    roll = int(input("Enter Roll No: "))
    date = input("Enter Date (YYYY-MM-DD): ")
    status = input("Enter New Status (P/A): ").upper()
    status = "Present" if status == "P" else "Absent"

    query = """
    UPDATE attendance
    SET status = %s
    WHERE rollno = %s AND attendance_date = %s
    """
    execute_query(query, (status, roll, date))
    print("Attendance updated successfully!")


# ---------------- EXPORT REPORT ---------------- #

def export_attendance():
    date = input("Enter Date (YYYY-MM-DD): ")
    query = """
    SELECT students.rollno, students.student_name, attendance.status
    FROM students
    JOIN attendance ON students.rollno = attendance.rollno
    WHERE attendance.attendance_date = %s
    """
    data = fetch_all(query, (date,))

    if not data:
        print("No attendance found for this date.")
        return

    filename = f"attendance_{date}.csv"
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Roll No", "Name", "Status"])
        writer.writerows(data)

    print(f"Attendance exported to {filename}")


# ---------------- MAIN PROGRAM LOOP ---------------- #

def main():
    while True:
        choice = menu()

        if choice == "1":
            manage_student()
        elif choice == "2":
            mark_attendance()
        elif choice == "3":
            view_report()
        elif choice == "4":
            modify_attendance()
        elif choice == "5":
            export_attendance()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice!")
main()
