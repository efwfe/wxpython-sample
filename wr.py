import xlsxwriter

with xlsxwriter.Workbook('hello.xlsx') as workbook:
    worksheet = workbook.add_worksheet()

    data_format1 = workbook.add_format({'bg_color': '#FFC7CE'})
    data_format2 = workbook.add_format({'bg_color': '#00C7CE'})

    for row in range(0, 10, 2):
        worksheet.set_row(row, cell_format=data_format1)
        worksheet.set_row(row + 1, cell_format=data_format2)
        worksheet.write(row, 0, "Hello")
        worksheet.write(row + 1, 0, "world")