import os
import subprocess

def calculate_sum_of_squares():
    result = sum(n ** 2 for n in range(1, 11))
    return result

def read_file_contents(file_path):
    with open(file_path, 'r') as file:
        return file.read()

if __name__ == "__main__":
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_file_dir, 'file_name.txt')

    result = calculate_sum_of_squares()
    print("Sum of squares:", result)

    command = ['cat', file_path]
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if process.returncode == 0:
        print("File contents:")
        print(process.stdout)
    else:
        print("Error occurred while reading file:", process.stderr)
