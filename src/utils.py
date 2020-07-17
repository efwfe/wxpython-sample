"""
收集目录下的文件信息，
生成wx对象

"""

import os
import wx


class FileHandler:

    def get_all_files(self, path):
        names = []
        for fn in os.listdir(path):
            name = os.path.join(path, fn)
            names.append(name)
        return name

    def extract_image_file(self, file_path):
        meta_data = file_path.split(os.sep)
        print(meta_data)