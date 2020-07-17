"""
收集目录下的文件信息，
生成wx对象

"""

import os
from collections import defaultdict
import random
# from clf import Parser


class FileHandler:

    """
    1.  获取文件的名称
    2。 获取文件夹名称，以及里面的文件名
    """
    # def __init__(self):
    #     self.parse = Parser()

    def extract_file(self, file_path):
        fn = file_path.split(os.sep)[-1]
        data = [
            ['5130001000000183825300','5130005009990129863892'],
            ['5130005009990129863895','5130005009990129863891'],
            ['5130005009990129863895','5130005009992129863895']
        ] 
        # data = self.parse.get_data_array(file_path)
        return fn, {"data":data, 'file_path':file_path}


    def extract_files(self, dir_path):
        dir_name = dir_path.split(os.sep)[-1]
        fns = [os.path.join(dir_path,i) for i in os.listdir(dir_path)]  
        
        results = []

        for fn in fns:
            data = self.extract_file(fn)
            results.append(data)

        return dir_name, results


    # def show_img(self, img_path):
    #     self.parse.show_img(img_path)