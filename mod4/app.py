from flask import Flask, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, ValidationError, Field
from wtforms.validators import InputRequired, Email
from typing import Optional
import subprocess
import shlex


app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False


#task 2 Валидатор должен принимать на вход параметры min и max — минимальная и максимальная длина, а также опциональный параметр message
class NumberLength:
    def __init__(self, min=None, max=None, message=None):
        self.message = message or 'Поле должно содержать от {} до {} символов.'.format(min, max)
        self.min = min
        self.max = max

    def __call__(self, form: FlaskForm, field: Field):
        data = field.data
        if len(str(data)) > self.max or len(str(data)) < self.min:
            raise ValidationError(message=self.message)


def number_length(min_length: int, max_length: int, message: Optional[str] = None):
    def _number_length(form: FlaskForm, field: Field):
        data = field.data
        if len(str(data)) > max_length or len(str(data)) < min_length:
            raise ValidationError(message=message or 'Поле должно содержать от {} до {} символов.'.format(min_length, max_length))

    return _number_length



#task1 В endpoint /registration добавьте все валидаторы, о которых говорилось в последнем видео
class RegistrationForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email()])
    phone = IntegerField(validators=[InputRequired(), NumberLength(min=10, max=12)])
    name = StringField(validators=[InputRequired()])
    address = StringField(validators=[InputRequired()])
    index = IntegerField(validators=[InputRequired()])
    comment = StringField()


@app.route("/registration", methods=["POST"])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        return "ОК"
    else:
        errors_list = form.errors
        return errors_list, 400


#task4 Напишите GET-endpoint /uptime, который в ответ на запрос будет выводить строку вида
#f"Current uptime is {UPTIME}"

@app.route('/uptime')
def get_uptime():
    command = ['uptime', '-p']
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    uptime = result.stdout.strip().replace('up ', '')
    return f'Current uptime is {uptime}'


# task 5 Напишите GET-endpoint /ps, который принимает на вход аргументы командной строки, а возвращает результат
# работы команды ps с этими аргументами.
@app.route('/ps', methods=['GET'])
def ps():
    args = request.args.getlist('arg')
    clean_args = [shlex.quote(arg) for arg in args]
    command = "ps " + " ".join(clean_args)
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        if result.returncode == 0:
            return f'<pre>{result.stdout}</pre>'
        else:
            return f'Команда завершена с ошибкой: {result.stderr}', 400
    except Exception as e:
        return f'Произошла ошибка при выполнении команды: {e}', 500

if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)