import sys

def get_mean_size(data):
    lines = data.strip().split('\n')[1:]
    total_size = 0
    num_files = 0

    for line in lines:
        tokens = line.split()
        if len(tokens) >= 5:
            file_size = int(tokens[4])
            total_size += file_size
            num_files += 1

    if num_files == 0:
        return 0
    else:
        return total_size / num_files

if __name__ == "__main__":
    data = sys.stdin.read()
    mean_size = get_mean_size(data)
    print(mean_size)
