import signal
from flask import Flask
import subprocess
import os

app = Flask(__name__)


#Задача 1. Освобождение порта
def check_port(port: int) -> list[int]:
    """Проверяет, используется ли указанный порт и возвращает список PID процессов, прослушивающих порт."""
    command = ['lsof', '-i', f'tcp:{port}']
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    pids = []
    for line in result.stdout.split('\n')[1:]:
        if line:
            pids.append(int(line.split()[1]))
    return pids

def kill_processes(pids: list[int]):
    """Завершает процессы с указанными PID."""
    for pid in pids:
        try:
            os.kill(pid, signal.SIGKILL)
            print(f"Процесс с PID {pid} завершен")
        except PermissionError:
            print(f"Нет разрешения на завершение процесса с PID {pid}")
        except ProcessLookupError:
            print(f"Процесс с PID {pid} не найден")

@app.route('/')
def index():
    return 'Все хорошо]'

if __name__ == '__main__':
    # Проверяем, используется ли порт 5000, и завершаем процессы, если да
    processes = check_port(5000)
    if processes:
        print(f"Порт 5000 уже используется процессами: {processes}. Попытка освободить порт...")
        kill_processes(processes)
    app.run(debug=False, port=5000)
