# -*- coding:utf-8 -*-
"""
@file name :  table
@description: 
@author:      张玳辉
@date :       2020/5/9-4:42 下午
"""

import xlsxwriter


# Create an new Excel file and add a worksheet.
workbook = xlsxwriter.Workbook('images.xlsx')
worksheet = workbook.add_worksheet()

# Widen the first column to make the text clearer.
worksheet.set_column('A:A', 30)

# Insert an image.
# worksheet.write('A2', 'Insert an image in a cell:')
# worksheet.insert_image('B2', 'python.png')
image_width = 140.0
image_height = 182.0

cell_width = 64.0
cell_height = 20.0

x_scale = cell_width/image_width
y_scale = cell_height/image_height

# Insert an image offset in the cell.
worksheet.insert_image('A1', 'sample.jpg', {'x_scale': 0.03, 'y_scale': 0.01})

# Insert an image with scaling.
# worksheet.write('A23', 'Insert a scaled image:')
# worksheet.insert_image('B23', 'python.png', {'x_scale': 0.5, 'y_scale': 0.5})

workbook.close()