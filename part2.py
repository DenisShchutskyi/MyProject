# -*- coding: UTF-8 -*-
import asyncio
import os
# import traceback
from PIL import Image


class MyImage(object):
    img: object = None
    path: str = 'FileNotFound'
    name_file: str = ''
    width: int = 0
    height: int = 0

    def __init__(self, path_to_file: str):
        try:
            self.img = Image.open(path_to_file)
            self.path = path_to_file
            self.name_file = path_to_file.split('\\')[-1]
            self.width = self.img.size[0]
            self.height = self.img.size[1]
        except IOError:
            # traceback.print_exc()
            pass

    def get_data_img(self):
        return {
            'path_to_img': self.path,
            'name_file': self.name_file,
            'width': self.width,
            'height': self.height
        }

    def __str__(self):
        return "{'path_to_img': +" + self.path + \
               ",'name_file':" + self.name_file +\
               ",'width':" + str(self.width) + \
               ",'height': " + str(self.height)+"}"


class MyClass(object):
    format_response: str = '<img src="{}" width="{}" height="{}" />'
    files_list: list = []  # список файлов
    count_thread: int = 2  # количество потоков по умолчанию
    current_value: int = 0  # стартовое значение

    def __init__(self,
                 list_files=None,
                 count_thread=2):
        if list_files:  # если список есть
            self.files_list = [{
                'file': MyImage(lf),
                'is_view': False
            } for lf in list_files]  # предобработка изображений чтоб знать какие файлы обработали
        try:
            self.count_thread = int(count_thread)  # проверка валидности количества потоков
        except ValueError:
            pass

    async def __work_function(self):
        while self.current_value < len(self.files_list):  # проход по списку файлов
            if self.files_list[self.current_value]['is_view']:  # проверка выводился ли данный файл
                self.current_value += 1
            else:
                self.files_list[self.current_value]['is_view'] = True  # отметить что файл обработан
                if self.files_list[self.current_value]['file'].img:  # проверка что вышло считать файл
                    tmp = self.files_list[self.current_value]['file'].get_data_img()  # получение данных изображения
                    print(self.format_response.format(tmp['name_file'],
                                                      tmp['width'],
                                                      tmp['height']))

    def run(self):
        print('__START__')
        loop = asyncio.get_event_loop()
        for _ in range(self.count_thread):  # создание указанное количества "потоков"
            loop.run_until_complete(self.__work_function())  # инициализация потока для функции
        loop.close()
        print("__END__")


if __name__ == '__main__':
    name_dir = os.curdir + '\\files_img'
    files = [name_dir + '\\'+f for f in os.listdir(name_dir)]
    tmp_ = MyClass(list_files=files,
                   count_thread=3)
    tmp_.run()
