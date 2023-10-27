import os
import sqlite3
import tkinter as tk
from tkinter import ttk

# Создание базы данных и таблицы сотрудников
class EmployeeDB:
    def init(self):
        self.conn = sqlite3.connect('employees.db')
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS employees (
                       id INTEGER PRIMARY KEY,
                       name TEXT,
                       phone TEXT,
                       email TEXT,
                       salary REAL
                       );
        """)
        self.conn.commit()

employee_db = EmployeeDB()

# Функция для отображения сотрудников в таблице
def show_employees():
    for row in tree.get_children():
        tree.delete(row)
    employee_db.c.execute('SELECT * FROM employees')
    employees = employee_db.c.fetchall()
    for employee in employees:
        tree.insert('', 'end', values=employee)

# Функция для добавления сотрудника
def add_employee():
    def save_employee():
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        salary = float(salary_entry.get())
        employee_db.c.execute('INSERT INTO employees (name, phone, email, salary) VALUES (?, ?, ?, ?)',
                              (name, phone, email, salary))
        employee_db.conn.commit()
        show_employees()
        add_window.destroy()

    add_window = tk.Toplevel(root)
    add_window.title('Добавить сотрудника')
    name_label = tk.Label(add_window, text='ФИО:')
    name_entry = tk.Entry(add_window)
    phone_label = tk.Label(add_window, text='Телефон:')
    phone_entry = tk.Entry(add_window)
    email_label = tk.Label(add_window, text='Email:')
    email_entry = tk.Entry(add_window)
    salary_label = tk.Label(add_window, text='Зарплата:')
    salary_entry = tk.Entry(add_window)
    save_button = tk.Button(add_window, text='Сохранить', command=save_employee)
    name_label.pack()
    name_entry.pack()
    phone_label.pack()
    phone_entry.pack()
    email_label.pack()
    email_entry.pack()
    salary_label.pack()
    salary_entry.pack()
    save_button.pack()

# Функция для обновления данных сотрудника
def update_employee():
    def save_employee():
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        salary = float(salary_entry.get())
        employee_db.c.execute('UPDATE employees SET name=?, phone=?, email=?, salary=? WHERE id=?',
                              (name, phone, email, salary, selected_id))
        employee_db.conn.commit()
        show_employees()
        update_window.destroy()

    selected_item = tree.selection()[0]
    selected_id = tree.item(selected_item)['values'][0]
    employee_db.c.execute('SELECT * FROM employees WHERE id=?', (selected_id,))
    employee = employee_db.c.fetchone()

    update_window = tk.Toplevel(root)
    update_window.title('Обновить сотрудника')
    name_label = tk.Label(update_window, text='ФИО:')
    name_entry = tk.Entry(update_window)
    name_entry.insert(0, employee[1])
    phone_label = tk.Label(update_window, text='Телефон:')
    phone_entry = tk.Entry(update_window)
    phone_entry.insert(0, employee[2])
    email_label = tk.Label(update_window, text='Email:')
    email_entry = tk.Entry(update_window)
    email_entry.insert(0, employee[3])
    salary_label = tk.Label(update_window, text='Зарплата:')
    salary_entry = tk.Entry(update_window)
    salary_entry.insert(0, employee[4])
    save_button = tk.Button(update_window, text='Сохранить', command=save_employee)
    name_label.pack()
    name_entry.pack()
    phone_label.pack()
    phone_entry.pack()
    email_label.pack()
    email_entry.pack()
    salary_label.pack()
    salary_entry.pack()
    save_button.pack()

# Функция для удаления сотрудников
def delete_employees():
    for selected_item in tree.selection():
        selected_id = tree.item(selected_item)['values'][0]
        employee_db.c.execute('DELETE FROM employees WHERE id=?', (selected_id,))
        employee_db.conn.commit()
        tree.delete(selected_item)

# Функция для поиска сотрудников
def search_employees():
    def search_employee():
        search_text = search_entry.get()
        employee_db.c.execute('SELECT * FROM employees WHERE name LIKE ?', ('%' + search_text + '%',))
        employees = employee_db.c.fetchall()
        for row in tree.get_children():
            tree.delete(row)
        for employee in employees:
            tree.insert('', 'end', values=employee)
        search_window.destroy()

    search_window = tk.Toplevel(root)
    search_window.title('Поиск сотрудников')
    search_label = tk.Label(search_window, text='Введите ФИО сотрудника:')
    search_entry = tk.Entry(search_window)
    search_button = tk.Button(search_window, text='Найти', command=search_employee)
    search_label.pack()
    search_entry.pack()
    search_button.pack()

# Функция для обновления данных в таблице
def refresh_table():
    show_employees()

# Создание главного окна приложения
root = tk.Tk()
root.title('Управление сотрудниками')

# Создание верхней панели с кнопками
toolbar = tk.Frame(root)

add_picture = tk.PhotoImage(file='img/add.png')
add_button = tk.Button(toolbar, command=add_employee, image=add_picture)

update_picture = tk.PhotoImage(file='img/update.png')
update_button = tk.Button(toolbar, command=update_employee, image=update_picture)

delete_picture = tk.PhotoImage(file='img/delete.png')
delete_button = tk.Button(toolbar, command=delete_employees, image=delete_picture)

search_picture = tk.PhotoImage(file='img/search.png')
search_button = tk.Button(toolbar, command=search_employees, image=search_picture)

refresh_picture = tk.PhotoImage(file='img/refresh.png')
refresh_button = tk.Button(toolbar, command=refresh_table, image=refresh_picture)

add_button.pack(side=tk.LEFT)
update_button.pack(side=tk.LEFT)
delete_button.pack(side=tk.LEFT)
search_button.pack(side=tk.LEFT)
refresh_button.pack(side=tk.LEFT)

toolbar.pack(side=tk.TOP, fill=tk.X)

# Создание таблицы для отображения сотрудников
tree = ttk.Treeview(root, columns=('id', 'name', 'phone', 'email', 'salary'), show='headings')
tree.heading('id', text='ID')
tree.heading('name', text='ФИО')

tree.heading('phone', text='Телефон')
tree.heading('email', text='Email')
tree.heading('salary', text='Зарплата')

tree.column('id', width=50)
tree.column('name', width=150)
tree.column('phone', width=150)
tree.column('email', width=150)
tree.column('salary', width=100)

tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Отображение сотрудников в таблице
show_employees()

# Запуск главного цикла приложения
root.mainloop()

# Закрытие базы данных
employee_db.conn.close()