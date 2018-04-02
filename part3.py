# -*- coding: UTF-8 -*-
import asyncio
import os
import traceback

from bs4 import BeautifulSoup
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
            traceback.print_exc()
            pass

    def get_data_img(self):
        return {
            'path_to_img': self.path,
            'name_file': self.name_file,
            'width': self.width,
            'height': self.height
        }


class MyParseHTMLs(object):
    default_width: int = 50
    default_height: int = 50
    count_thread: int = 2
    list_path_to_page: list = []
    current_value: int = 0

    def __init__(self,
                 list_path=None,
                 count_thread=2):
        self.list_path_to_page = [
            {'file': l,
             'is_parse': False} for l in list_path]
        try:
            self.count_thread = int(count_thread)
        except ValueError:
            pass

    def run(self):
        print('__START__')
        loop = asyncio.get_event_loop()
        for _ in range(self.count_thread):
            loop.run_until_complete(self.__parse_page())
        loop.close()

        print("__END__")

    async def __parse_page(self):
        while self.current_value < len(self.list_path_to_page):
            if self.list_path_to_page[self.current_value]['is_parse']:
                self.current_value += 1
            else:
                self.list_path_to_page[self.current_value]['is_parse'] = True
                path_to_page = self.list_path_to_page[self.current_value]['file']
                is_update_file = False
                dirs = path_to_page.split('\\')
                # name_file = dirs[-1]
                path_to_dirs = '\\'.join(dirs[:-1])
                soup = BeautifulSoup(open(path_to_page), 'html.parser')
                for i, val in enumerate(soup.find_all('img')):
                    name_img = val['src']
                    img = None
                    try:
                        val['width']
                    except KeyError:
                        img = MyImage(path_to_dirs + '\\' + name_img)
                        if img.img:
                            val['width'] = img.width
                        else:
                            val['width'] = self.default_width
                        is_update_file = True
                    try:
                        val['height']
                    except KeyError:
                        if img:
                            pass
                        else:
                            img = MyImage(path_to_dirs + '\\' + name_img)
                        if img.img:
                            val['height'] = img.height
                        else:
                            val['height'] = self.default_height
                        is_update_file = True
                        # print(i)
                if is_update_file:
                    text = str(soup.prettify())
                    # print(text)
                    with open(path_to_page, 'w') as f:
                        f.write(text)


if __name__ == '__main__':
    name_dir = os.curdir + '\\files_html'
    files = [name_dir + '\\' + f for f in os.listdir(name_dir) if f.endswith('.html')]
    MyParseHTMLs(files, ).run()





