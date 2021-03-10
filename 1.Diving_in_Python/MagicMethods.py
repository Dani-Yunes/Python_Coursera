import tempfile
import os

class File:

    def __init__(self, full_filepath): #Инициализация
        self.full_filepath = full_filepath
        self.seek = 0

    def __str__(self): #Вывод
        return self.full_filepath

    def __iter__(self):
        return self

    def __next__(self): #Итерация по строкам
        with open(self.full_filepath) as f:
            f.seek(self.seek)
            result = f.readline()
            self.seek = f.tell()
            if result == '':
                raise StopIteration
            return result

    def __add__(self, second_file): #Сложение двух File-ов
        new_path = os.path.join(tempfile.gettempdir(), 'new_file.txt')
        with open(new_path, 'w') as f:
            for line in self:
                f.write(line)
            for line in second_file:
                f.write(line)
            f.write('\n')
        return File(new_path)


    def write(self, text):
        with open(self.full_filepath, 'w') as f:
            f.write(text)



