def get_summary_rss(file_path):
    total_memory = 0
    with open(file_path, 'r') as f:
        lines = f.readlines()[1:]  # Пропускаем заголовок
        for line in lines:
            columns = line.split()
            rss_memory = int(columns[5])  # Индекс 5 соответствует столбцу RSS
            total_memory += rss_memory

    # Конвертируем в человекочитаемый формат
    memory_suffixes = ['B', 'KiB', 'MiB', 'GiB', 'TiB']
    memory_index = 0
    while total_memory >= 1024 and memory_index < len(memory_suffixes) - 1:
        total_memory /= 1024
        memory_index += 1

    return f"Total memory used: {total_memory:.2f} {memory_suffixes[memory_index]}"


if __name__ == '__main__':
    file_path = 'output_file.txt'
    print(get_summary_rss(file_path))
