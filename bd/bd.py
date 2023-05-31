import psycopg2
from .config import host, user, password, db_name
import secrets
import bcrypt
import csv

# Хэширование пароля
def hash_password(password):
    # преобразуем строку пароля в байтовую строку
    new_password = password.encode('utf-8')

    # генерируем соль для хэширования пароля
    salt = bcrypt.gensalt()

    # хэшируем пароль с помощью соли
    hashed_password = bcrypt.hashpw(new_password, salt)

    # возвращаем хэш пароля
    return hashed_password.decode('utf-8')

# Создаём секретный ключ
def generate_secret_key(cursor):
    while True:
        # Генерация случайного ключа
        sec_key = secrets.token_hex(8)

        # Проверка на уникальность
        cursor.execute("SELECT COUNT(*) FROM users WHERE key = %s", (sec_key,))
        count = cursor.fetchone()[0]

        if count == 0:
            return sec_key

def check_login(input_key):
    # Параметры таблицы
    table_name = "users"
    key_column = "key"
    password_hash_column = "password_hash"

    access = False

    try:
        # Установление соединения с базой данных
        connection = psycopg2.connect(host=host, database=db_name, user=user, password=password)

        # Создание объекта "курсор"
        cursor = connection.cursor()

        # Поиск пользователя по ключу
        select_query = f"SELECT {key_column} FROM {table_name} WHERE {key_column} = %s;"
        cursor.execute(select_query, (input_key,))
        row = cursor.fetchone()

        if row:
            key_nedd = row[0]
            print("Ключ верный")

            access = True
        else:
            print("Неверный ключ")

    except (Exception, psycopg2.Error) as error:
        print("Ошибка при выполнении запроса к базе данных:", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return access

def insert_users_from_csv(cursor, file_path):
    column_names = ["username", "password", "key"]

    # Открытие CSV файла и чтение данных
    with open(file_path, "r") as file:
        csv_data = csv.reader(file)
        next(csv_data)  # Пропуск заголовков столбцов в CSV файле

        # Итерация по строкам CSV файла
        for row in csv_data:
            username = row[0]
            password = hash_password(row[1])

            # Создание секретного ключа
            key = generate_secret_key(cursor)

            # Вставка данных из CSV файла в таблицу
            insert_query = f"INSERT INTO users ({', '.join(column_names)}) VALUES (%s, %s, %s);"
            values = (username, password, key)

            cursor.execute(insert_query, values)

        print("Пользователи успешно добавлены")

try:
    # Подключаемся к базе
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True

    cursor = connection.cursor()

    csv_file_path = "data.csv"
    insert_users_from_csv(cursor, csv_file_path)

except Exception as ex:
    print("Error while working with PostgreSQL:", ex)

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()

# try:
#     # Создаём таблицу
#     connection = psycopg2.connect(
#         host=host,
#         user=user,
#         password=password,
#         database=db_name
#     )
#     connection.autocommit = True
#
#     with connection.cursor() as cursor:
#         create_table_query = """
#             CREATE TABLE IF NOT EXISTS users (
#                 id SERIAL PRIMARY KEY,
#                 username VARCHAR(255) NOT NULL,
#                 password VARCHAR(255) NOT NULL,
#                 key VARCHAR(255) NOT NULL
#             );
#             """
#         cursor.execute(create_table_query)
#
#         print("Таблица успешно создана")
#
# except Exception as ex:
#     print("Error while working with PostgreSQL:", ex)
#
# finally:
#     if cursor:
#         cursor.close()
#     if connection:
#         connection.close()
