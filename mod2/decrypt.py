import sys

def decrypt(input_string):
    result = []
    i = 0
    while i < len(input_string):
        if input_string[i:i + 2] == "..":
            if result:
                result.pop()
            i += 2
        elif input_string[i] == ".":
            i += 1
        else:
            result.append(input_string[i])
            i += 1
    return ''.join(result)

if __name__ == '__main__':
    data = sys.stdin.read()
    print(decrypt(data))