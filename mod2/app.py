from flask import Flask, request, jsonify
from get_summary_rss import get_summary_rss
from get_mean_size import get_mean_size
from decrypt import decrypt
from datetime import datetime
from get_day import get_day_of_week_name
from collections import defaultdict
import os


app = Flask(__name__)


@app.route('/')
def index():
    return "Hello World"


#задача 1
@app.route('/summary_rss', methods=['GET', 'POST'])
def summary_rss():
    result = get_summary_rss('output_file.txt')
    return result


#задача 2
@app.route('/get_mean_size', methods=['POST'])
def calculate_mean_size():
    data = request.data.decode('utf-8')
    mean_size = get_mean_size(data)
    return str(mean_size)

#задача 3
@app.route('/decrypt', methods=['POST'])
def decrypt_message():
    data = request.data.decode('utf-8')
    result = decrypt(data)
    return result

#задача 4
@app.route('/hello-world/<name>')
def hello(name):
    weekday = datetime.today().weekday()
    day_of_week_name = get_day_of_week_name(weekday)
    return f"Привет, {name}. {day_of_week_name}!"

#задача 5
@app.route('/max_number/<path:numbers>')
def max_number(numbers):
    numbers_list = numbers.split('/')
    try:
        numbers_list = [int(num) for num in numbers_list]
    except ValueError:
        return "Некорректные параметры: ожидались числа", 400
    max_num = max(numbers_list)
    return f"Максимальное переданное число: <i>{max_num}</i>"


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def get_absolute_path(relative_path):
    return os.path.join(BASE_DIR, relative_path)

#задача 6
@app.route('/preview/<int:size>/<path:relative_path>')
def file_preview(size, relative_path):
    abs_path = get_absolute_path(relative_path)

    with open(abs_path, 'r') as file:
        result_text = file.read(size)
        result_size = len(result_text)

    return f"<b>{abs_path}</b> {result_size}<br>{result_text}"


#задача 7
# Хранилище данных о расходах
storage = defaultdict(lambda: defaultdict(int))


@app.route('/add/<date>/<int:number>')
def add_expense(date, number):
    try:
        year = int(date[:4])
        month = int(date[4:6])
        day = int(date[6:])
        if month < 1 or month > 12 or day < 1 or day > 31:
            raise ValueError("Неправильный формат даты")
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    storage.setdefault(year, {}).setdefault(month, 0)
    storage[year][month] += number

    return "Расход успешно добавлен"


@app.route('/calculate/<int:year>')
def calculate_year(year):
    if year not in storage:
        return jsonify({"error": "Нет данных для выбранного года"}), 404

    total_expense = sum(storage[year].values())
    return jsonify({"year": year, "total_expense": total_expense})


@app.route('/calculate/<int:year>/<int:month>')
def calculate_month(year, month):
    if year not in storage or month not in storage[year]:
        return jsonify({"error": "Нет данных для выбранного месяца и года"}), 404

    total_expense = storage[year][month]
    return jsonify({"year": year, "month": month, "total_expense": total_expense})

if __name__ == '__main__':
    app.run(debug=True)