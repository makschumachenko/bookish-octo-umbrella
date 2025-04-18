from flask import Flask
from datetime import datetime
import random

app = Flask(__name__)


cars_list = ["Chevrolet", "Renault", "Ford", "Lada"]
cats_list = ["корниш-рекс", "русская голубая", "шотландская вислоухая", "мейн-кун", "манчкин"]
counter_visits = 0


# Задача 1
@app.route('/hello_world')
def hello_world():
    return "Привет, мир!"

# Задача 2
@app.route('/cars')
def cars():
    return ', '.join(cars_list)

# Задача 3
@app.route('/cats')
def cats():
    return random.choice(cats_list)

# Задача 4
@app.route('/get_time/now')
def get_time_now():
    current_time = datetime.now().strftime('%H:%M:%S')
    return "Текущее время: " + current_time

# Задача 5
@app.route('/get_time/future')
def get_time_future():
    future_time = (datetime.now() + timedelta(hours=1)).strftime('%H:%M:%S')
    return 'Через час будет: ' + future_time

# Задача 6
def get_random_word():
    return random.choice(book_words)

@app.route('/get_random_word')
def random_word():
    return get_random_word()

# Задача 7
@app.route('/counter')
def counter():
    global counter_visits
    counter_visits += 1
    return str(counter_visits)


if __name__ == '__main__':
    app.run(debug=True)