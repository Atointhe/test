import tkinter as tk
from tkinter import messagebox, ttk
import json
import psycopg2
import MySQLdb  # Для примера добавим поддержку MySQL


def save_settings():
    db_type = db_type_var.get()
    db_url = url_entry.get()
    db_port = port_entry.get()
    db_user = user_entry.get()
    db_password = password_entry.get()

    if not db_type or not db_url or not db_port or not db_user or not db_password:
        messagebox.showwarning("Внимание", "Пожалуйста, заполните все поля.")
        return

    settings = {
        "db_type": db_type,
        "db_url": db_url,
        "db_port": db_port,
        "db_user": db_user,
        "db_password": db_password
    }

    try:
        with open("config.json", "w") as config_file:
            json.dump(settings, config_file, indent=4)
        messagebox.showinfo("Настройки", "Настройки сохранены успешно.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить настройки:\n{e}")


def test_connection():
    db_type = db_type_var.get()
    db_url = url_entry.get()
    db_port = port_entry.get()
    db_user = user_entry.get()
    db_password = password_entry.get()

    if not db_type or not db_url or not db_port or not db_user or not db_password:
        messagebox.showwarning("Внимание", "Пожалуйста, заполните все поля для теста подключения.")
        return

    try:
        if db_type == "PostgreSQL":
            conn = psycopg2.connect(
                host=db_url,
                port=db_port,
                user=db_user,
                password=db_password,
                connect_timeout=5
            )
        elif db_type == "MySQL":
            conn = mysql.connector.connect(
                host=db_url,
                port=int(db_port),
                user=db_user,
                password=db_password,
                connection_timeout=5
            )
        else:
            messagebox.showerror("Ошибка", "Не поддерживаемый тип базы данных.")
            return
        conn.close()
        messagebox.showinfo("Тест подключения", "Подключение прошло успешно!")
    except Exception as e:
        messagebox.showerror("Тест подключения", f"Не удалось подключиться к базе данных:\n{e}")


# Создание главного окна
root = tk.Tk()
root.title("Настройки подключения к БД")

# Тип базы данных
tk.Label(root, text="Тип базы данных:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
db_type_var = tk.StringVar()
db_type_combo = ttk.Combobox(root, textvariable=db_type_var, values=["PostgreSQL", "MySQL"], state="readonly", width=27)
db_type_combo.grid(row=0, column=1, padx=10, pady=5)
db_type_combo.current(0)  # Устанавливаем значение по умолчанию

# Адрес подключения
tk.Label(root, text="Адрес подключения:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
url_entry = tk.Entry(root, width=30)
url_entry.grid(row=1, column=1, padx=10, pady=5)

# Порт подключения
tk.Label(root, text="Порт:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
port_entry = tk.Entry(root, width=30)
port_entry.grid(row=2, column=1, padx=10, pady=5)
port_entry.insert(0, "5432" if db_type_var.get() == "PostgreSQL" else "3306")  # Значения по умолчанию

# Логин
tk.Label(root, text="Логин:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
user_entry = tk.Entry(root, width=30)
user_entry.grid(row=3, column=1, padx=10, pady=5)

# Пароль
tk.Label(root, text="Пароль:").grid(row=4, column=0, padx=10, pady=5, sticky='e')
password_entry = tk.Entry(root, show="*", width=30)
password_entry.grid(row=4, column=1, padx=10, pady=5)

# Кнопки для сохранения настроек и тестирования подключения
save_button = tk.Button(root, text="Сохранить", command=save_settings, width=15)
save_button.grid(row=5, column=1, padx=10, pady=10, sticky='e')

test_button = tk.Button(root, text="Тестировать подключение", command=test_connection, width=20)
test_button.grid(row=6, column=1, padx=10, pady=5, sticky='e')

# Запуск главного цикла приложения
root.mainloop()
