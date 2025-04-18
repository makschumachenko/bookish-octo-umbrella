import subprocess
import logging

from flask import Flask, jsonify, request
from flask_wtf import FlaskForm
from wtforms.fields.simple import *
from wtforms.fields.numeric import *
from wtforms.validators import InputRequired, NumberRange

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CodeForm(FlaskForm):
    code = StringField('Код', validators=[InputRequired(message="Код обязателен для заполнения")])
    timeout = IntegerField('Таймаут', validators=[InputRequired(message="Таймаут обязателен для заполнения"),
                                                  NumberRange(min=1, max=30, message="Таймаут должен быть от 1 до 30")])


def run_code(code: str, timeout: int):
    command = ['prlimit', '--nproc=1:1', 'python', '-c', code]
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        result, error = process.communicate(timeout=timeout)
        if result:
            return result
        return f'Ошибка при попытке запуска кода:\n{error}', 400
    except subprocess.TimeoutExpired:
        process.kill()
        process.communicate()
        return f'Во время выполнения кода был превышен лимит времени: {timeout} секунд ', 500
    except Exception as e:
        logger.error(f"Ошибка выполнения кода: {e}")
        return "Произошла ошибка при выполнении кода", 500


@app.route('/codeRunner', methods=['POST'])
def execute_code():
    form = CodeForm(request.form)
    if form.validate():
        user_code = form.code.data
        user_timeout = form.timeout.data
        return run_code(code=user_code, timeout=user_timeout)
    else:
        errors = {key: [error for error in value] for key, value in form.errors.items()}
        return jsonify({'error': 'Неверный ввод', 'errors': errors}), 422


if __name__ == '__main__':
    app.config['WTF_CSRF_ENABLED'] = True
    app.run(debug=True, port=5467)
