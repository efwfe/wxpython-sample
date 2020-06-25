# -*- coding:utf-8 -*-
"""
@file name :  main
@description: 
@author:      张玳辉
@date :       2020/5/9-5:15 下午
"""

import xlsxwriter
from pyzbar.pyzbar import decode
from PIL import Image

img = Image.open('sample.jpg')

result = decode(img)
datas, heights = [], set()
for i in result:
    datas.append(str(i.data.decode()))
    heights.add(str(i.polygon[0].y)[0])

seg, _ = divmod(len(datas), len(heights))
if _ > 0: seg += 1


def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def save(datas, seg):
    workbook = xlsxwriter.Workbook('images.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0,0, 'sample.jpg')
    x, y = 0, 1
    for ind, item in enumerate(batch(datas, n=seg)):
        for y_ind, word in enumerate(item):
            worksheet.write(x + ind, y + y_ind, word)
    workbook.close()

if __name__ == '__main__':
    save(datas, seg)
