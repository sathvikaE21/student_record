import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


db = mysql.connector.connect(
    host="mysql-db",
    port=3306,
    user="root",
    password="Chikky21#",
    database="student_db"
)
cursor = db.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    roll_no VARCHAR(50),
    grade VARCHAR(10)
)
""")
db.commit()


def add_student():
    name = name_var.get()
    roll = roll_var.get()
    grade = grade_var.get()
    if not name or not roll or not grade:
        messagebox.showwarning("Input Error", "All fields required")
        return
    cursor.execute("INSERT INTO students (name, roll_no, grade) VALUES (%s, %s, %s)", (name, roll, grade))
    db.commit()
    messagebox.showinfo("Success", "Student added successfully")
    fetch_students()
    clear_fields()

def fetch_students():
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", tk.END, values=row)

def delete_student():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Error", "Select a student to delete")
        return
    item = tree.item(selected[0])
    student_id = item['values'][0]
    cursor.execute("DELETE FROM students WHERE id=%s", (student_id,))
    db.commit()
    fetch_students()
    clear_fields()

def update_student():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Error", "Select a student to update")
        return
    item = tree.item(selected[0])
    student_id = item['values'][0]

    name = name_var.get()
    roll = roll_var.get()
    grade = grade_var.get()

    if not name or not roll or not grade:
        messagebox.showwarning("Input Error", "All fields required")
        return

    cursor.execute("""
        UPDATE students SET name=%s, roll_no=%s, grade=%s WHERE id=%s
    """, (name, roll, grade, student_id))
    db.commit()
    messagebox.showinfo("Success", "Student updated successfully")
    fetch_students()
    clear_fields()

def search_student():
    query = search_var.get().strip()
    if not query:
        messagebox.showwarning("Search Error", "Enter Roll No to search")
        return
    for row in tree.get_children():
        if tree.item(row)['values'][2] == query:
            tree.selection_set(row)
            tree.focus(row)
            return
    messagebox.showinfo("Not Found", "No student with that Roll No")

def sort_students():
    records = [tree.item(row)['values'] for row in tree.get_children()]
    records.sort(key=lambda x: x[1])  # Sort by Name
    tree.delete(*tree.get_children())
    for record in records:
        tree.insert("", tk.END, values=record)

def on_row_select(event):
    selected = tree.selection()
    if selected:
        item = tree.item(selected[0])
        values = item['values']
        name_var.set(values[1])
        roll_var.set(values[2])
        grade_var.set(values[3])

def clear_fields():
    name_var.set("")
    roll_var.set("")
    grade_var.set("")
    search_var.set("")


root = tk.Tk()
root.title("Student Record Management")
root.geometry("700x550")
root.configure(bg="#fdf6f0")  


style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#fdf6f0", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6, background="#d88c5c", foreground="white")
style.map("TButton", background=[("active", "#e09b6c")])
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#d88c5c", foreground="white")
style.configure("Treeview", rowheight=25, background="#fffaf5", fieldbackground="#fffaf5", foreground="#333")


name_var = tk.StringVar()
roll_var = tk.StringVar()
grade_var = tk.StringVar()
search_var = tk.StringVar()


tk.Label(root, text="Name").grid(row=0, column=0, padx=10, pady=5, sticky="w")
tk.Label(root, text="Roll No").grid(row=1, column=0, padx=10, pady=5, sticky="w")
tk.Label(root, text="Grade").grid(row=2, column=0, padx=10, pady=5, sticky="w")

tk.Entry(root, textvariable=name_var, width=30).grid(row=0, column=1, padx=10, pady=5)
tk.Entry(root, textvariable=roll_var, width=30).grid(row=1, column=1, padx=10, pady=5)
tk.Entry(root, textvariable=grade_var, width=30).grid(row=2, column=1, padx=10, pady=5)


ttk.Button(root, text="Add Student", command=add_student).grid(row=3, column=0, padx=10, pady=10)
ttk.Button(root, text="Delete Student", command=delete_student).grid(row=3, column=1, padx=10, pady=10)
ttk.Button(root, text="Update Student", command=update_student).grid(row=3, column=2, padx=10, pady=10)

ttk.Button(root, text="Sort by Name", command=sort_students).grid(row=4, column=0, padx=10, pady=5)
ttk.Button(root, text="Search Roll No", command=search_student).grid(row=4, column=1, padx=10, pady=5)
ttk.Button(root, text="Clear Fields", command=clear_fields).grid(row=4, column=2, padx=10, pady=5)

tk.Entry(root, textvariable=search_var, width=30).grid(row=5, column=0, columnspan=3, padx=10, pady=5)

tree = ttk.Treeview(root, columns=("ID", "Name", "Roll", "Grade"), show="headings")
for col in ("ID", "Name", "Roll", "Grade"):
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=150)
tree.grid(row=6, column=0, columnspan=3, padx=10, pady=10)
tree.bind("<<TreeviewSelect>>", on_row_select)

fetch_students()
root.mainloop()