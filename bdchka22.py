import sqlite3

def connect_to_db():
    try:
        connection = sqlite3.connect("company.db")
        print("Подключено")
        return connection
    except sqlite3.Error as err:
        print(f"Ошибка: {err}")
        return None

def create_database():
    try:
        connection = sqlite3.connect("company.db")
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                birth_date TEXT NOT NULL,
                position TEXT NOT NULL,
                department TEXT NOT NULL,
                salary REAL NOT NULL
            )
        ''')
        connection.commit()
        print("База данных и таблица созданы.")
    except sqlite3.Error as err:
        print(f"Ошибка: {err}")
    finally:
        cursor.close()
        connection.close()

def add_employee(connection, name, birth_date, position, department, salary):
    try:
        cursor = connection.cursor()
        sql_query = """
        INSERT INTO employees (name, birth_date, position, department, salary)
        VALUES (?, ?, ?, ?, ?);
        """
        cursor.execute(sql_query, (name, birth_date, position, department, salary))
        connection.commit()
        print(f"Сотрудник {name} добавлен.")
    except sqlite3.Error as err:
        print(f"Ошибка: {err}")
    finally:
        cursor.close()
connection = connect_to_db()
if connection:
        add_employee(connection, "Иван Иванов", "1985-07-15", "Менеджер", "Продажи", 75000.00)
        add_employee(connection, "Дмитрий Сергеевич", "1999-10-12", "Разработчик", "IT", 80000.00)
        add_employee(connection, "Егор Ткаченко", "2004-05-20", "Аналитик", "Маркетинг", 60000.00)

def get_all_employees(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM employees;")
        employees = cursor.fetchall()

        if employees:
            print("Список сотрудников:")
            for emp in employees:
                print(emp)
        else:
            print("Нет сотрудников в базе данных.")
    except sqlite3.Error as err:
        print(f"Ошибка: {err}")
    finally:
        cursor.close()

def remove_employee(connection, emp_id):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM employees WHERE id = ?;", (emp_id,))
        connection.commit()
        print(f"Сотрудник с ID {emp_id} удален.")
    except sqlite3.Error as err:
        print(f"Ошибка: {err}")
    finally:
        cursor.close()

def search_employees(connection, search_term):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM employees WHERE name LIKE ? OR position LIKE ? OR department LIKE ?;",
                       (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        employees = cursor.fetchall()

        if employees:
            print("Результаты поиска:")
            for emp in employees:
                print(emp)
        else:
            print("Ничего не найдено.")
    except sqlite3.Error as err:
        print(f"Ошибка: {err}")
    finally:
        cursor.close()

def update_employee(connection, emp_id, name, birth_date, position, department, salary):
    try:
        cursor = connection.cursor()
        print(f"Обновление сотрудника ID {emp_id} ")
        cursor.execute('''
            UPDATE employees SET name = ?, birth_date = ?, position = ?, department = ?, salary = ?
            WHERE id = ?;
        ''', (name, birth_date, position, department, salary, emp_id))
        connection.commit()
        print(f"Данные сотрудника с ID {emp_id} обновлены.")
    except sqlite3.Error as err:
        print(f"Ошибка при обновлении: {err}")
    finally:
        if cursor:
            cursor.close()

def collect_statistics(connection):
    try:
        cursor = connection.cursor()

        cursor.execute("SELECT department, COUNT(*) FROM employees GROUP BY department;")
        department_distribution = cursor.fetchall()

        if department_distribution:
            print("\nРаспределение сотрудников по отделам:")
            for dept in department_distribution:

                print(f"Отдел: {dept[0]}, Количество: {dept[1]}")
            else:
                print("Нет сотрудников для статистики по отделам.")

            cursor.execute("SELECT AVG(salary) FROM employees;")
            average_salary = cursor.fetchone()[0]

            if average_salary is not None:
                print(f"\nСредняя зарплата: {average_salary:.2f}")
            else:
                print("Нет сотрудников для расчёта средней зарплаты.")
    except sqlite3.Error as err:
        print(f"Ошибка: {err}")
    finally:
        cursor.close()

def menu():
    connection = connect_to_db()
    while True:
        print("\nКонсольное меню:")
        print("1. Добавить сотрудника")
        print("2. Удалить сотрудника")
        print("3. Поиск сотрудника")
        print("4. Обновить данные сотрудника")
        print("5. Просмотр всех сотрудников")
        print("6. Сбор статистики")
        print("7. Выход")

        choice = input("Выберите действие (1-7): ")

        if choice == '1':
            name = input("Имя: ")
            birth_date = input("Дата рождения (YYYY-MM-DD): ")
            position = input("Должность: ")
            department = input("Отдел: ")
            salary = float(input("Зарплата: "))
            add_employee(connection, name, birth_date, position, department, salary)

        elif choice == '2':
            emp_id = int(input("Введите ID сотрудника для удаления: "))
            remove_employee(connection, emp_id)

        elif choice == '3':
            search_term = input("Введите имя и фамилию, должность или отдел для поиска: ")
            search_employees(connection, search_term)

        elif choice == '4':
            emp_id = int(input("Введите ID сотрудника для обновления: "))
            name = input("Новое имя и фамилия: ")
            birth_date = input("Новая дата рождения (YYYY-MM-DD): ")
            position = input("Новая должность: ")
            department = input("Новый отдел: ")
            salary = float(input("Новая зарплата: "))
            update_employee(connection, emp_id, name, birth_date, position, department, salary)

        elif choice == '5':
            get_all_employees(connection)

        elif choice == '6':
            collect_statistics(connection)

        elif choice == '7':
            connection.close()
            break

        else:
            print("Ошибка. Выберите действие от 1 до 7.")

menu()