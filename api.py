import json

from flask import Flask, request, jsonify
import psycopg2

from pagination import my_parse_funk

app = Flask(__name__)

DB_HOST = 'localhost'
DB_NAME = 'your_database'
DB_USER = 'postgres'
DB_PASS = 'qwertyzxc'

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

# Функция для создания таблицы, если она не существует
def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS parsed_data (
            id SERIAL PRIMARY KEY,
            url TEXT NOT NULL,
            title TEXT,
            content TEXT
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/parse', methods=['GET'])
def parse():
    # Вызов вашей функции парсинга
    result = my_parse_funk('MID_SF', 'Z_X_C_TblCHKA_TblCHKA_BKB', 1, 1)

    # Сохранение результата в базу данных
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO parsed_data (data) VALUES (%s)',
        (json.dumps(result),)  # Преобразуем список словарей в JSON строку
    )
    conn.commit()
    cur.close()
    conn.close()

    # Сохранение результата в файл (опционально)
    with open('output.json', 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=4)

    # Возвращаем результат в виде JSON
    return jsonify(result)

@app.route('/data', methods=['GET'])
def get_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM parsed_data')
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Преобразование данных в JSON
    data = []
    for row in rows:
        data.append({
            "id": row[0],
            "data": row[1]  # Данные уже в формате JSONB
        })

    return jsonify(data)

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
