import tempfile
import os
import uuid

class File:

    def __init__(self, full_filepath): #Инициализация
        if os.path.exists(full_filepath):
            pass
        else:
            with open(full_filepath, 'w') as f:
                pass
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
                self.seek = 0
                raise StopIteration
            return result

    def read(self): #Чтение из файла
        with open(self.full_filepath, 'r') as f:
            return f.read()


    def __add__(self, second_file): #Сложение двух File-ов
        new_path = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
        with open(new_path, 'w') as f:
            for line in self:
                f.write(line)
            for line in second_file:
                f.write(line)
        return File(new_path)


    def write(self, text):
        with open(self.full_filepath, 'w') as f:
            f.write(text)



