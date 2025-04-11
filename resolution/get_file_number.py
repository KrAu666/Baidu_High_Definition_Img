import os

def file_name_number(word):
    file = os.listdir(f'img/{word}')
    if file != []:
        file = [int(i.split('.')[0]) for i in file]
        file.sort()
        max_number = file[-1]
        return max_number + 1
    else:
        return 0
