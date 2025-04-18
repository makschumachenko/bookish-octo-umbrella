import os


def get_preview(size, relative_path):
    abs_path = os.path.abspath(relative_path)

    with open(abs_path, 'r') as file:
        result_text = file.read(size)
        result_size = len(result_text)

    return abs_path, result_size, result_text
