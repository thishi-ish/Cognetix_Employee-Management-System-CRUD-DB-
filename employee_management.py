import sqlite3
import re

DB_FILE = "employees.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS employees (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            department TEXT,
            salary REAL
        )"""
    )
    conn.commit()
    conn.close()

def is_valid_email(email):
    # very simple regex for email validation
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def add_employee():
    emp_id = input("Enter Employee ID: ").strip()
    name = input("Enter Name: ").strip()
    email = input("Enter Email: ").strip()
    department = input("Enter Department: ").strip()
    salary_input = input("Enter Salary: ").strip()

    if not emp_id or not name or not email:
        print("ID, Name, and Email are required.")
        return

    if not is_valid_email(email):
        print("Invalid email format.")
        return

    try:
        salary = float(salary_input) if salary_input else 0.0
    except ValueError:
        print("Invalid salary. Use numbers only.")
        return

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    # check duplicate
    cur.execute("SELECT id FROM employees WHERE id = ?", (emp_id,))
    if cur.fetchone():
        print("Employee with this ID already exists.")
        conn.close()
        return

    cur.execute(
        "INSERT INTO employees (id, name, email, department, salary) VALUES (?, ?, ?, ?, ?)",
        (emp_id, name, email, department, salary)
    )
    conn.commit()
    conn.close()
    print("✔ Employee added successfully.")

def view_employees():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, department, salary FROM employees")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No employees found.")
        return

    print("\n--- Employee List ---")
    for r in rows:
        print(f"ID: {r[0]}, Name: {r[1]}, Email: {r[2]}, Dept: {r[3]}, Salary: {r[4]}")

def update_employee():
    emp_id = input("Enter Employee ID to update: ").strip()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, department, salary FROM employees WHERE id = ?", (emp_id,))
    row = cur.fetchone()
    if not row:
        print("Employee not found.")
        conn.close()
        return

    print("Leave field blank to keep current value.")
    name = input(f"Name [{row[1]}]: ").strip() or row[1]
    email = input(f"Email [{row[2]}]: ").strip() or row[2]
    department = input(f"Department [{row[3]}]: ").strip() or row[3]
    salary_input = input(f"Salary [{row[4]}]: ").strip()
    salary = row[4]
    if salary_input:
        try:
            salary = float(salary_input)
        except ValueError:
            print("Invalid salary. Update canceled.")
            conn.close()
            return

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("Invalid email format. Update canceled.")
        conn.close()
        return

    cur.execute(
        "UPDATE employees SET name = ?, email = ?, department = ?, salary = ? WHERE id = ?",
        (name, email, department, salary, emp_id)
    )
    conn.commit()
    conn.close()
    print("✔ Employee updated.")

def delete_employee():
    emp_id = input("Enter Employee ID to delete: ").strip()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id FROM employees WHERE id = ?", (emp_id,))
    if not cur.fetchone():
        print("Employee not found.")
        conn.close()
        return

    cur.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
    conn.commit()
    conn.close()
    print("✔ Employee deleted.")

def main():
    init_db()
    while True:
        print("\n===== EMPLOYEE MANAGEMENT =====")
        print("1. Add Employee")
        print("2. View Employees")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("5. Exit")
        choice = input("Choose (1-5): ").strip()
        if choice == "1":
            add_employee()
        elif choice == "2":
            view_employees()
        elif choice == "3":
            update_employee()
        elif choice == "4":
            delete_employee()
        elif choice == "5":
            print(" Exiting.")
            break
        else:
            print("Invalid choice.")
if __name__ == "__main__":
    main()
