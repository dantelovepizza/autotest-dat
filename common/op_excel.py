import openpyxl


class ExcelHandler:
    def __init__(self, file):
        self.file = file
        self.wb = openpyxl.load_workbook(self.file)

    def _open_excel(self, sheet_name):
        """打开工作簿指定sheet页，返回sheet对象"""
        sheet = self.wb[sheet_name]
        return sheet

    def header_excel(self, sheet_name):
        """获取excel表头"""
        sheet = self._open_excel(sheet_name)
        header = []
        # 遍历第一行
        for column in sheet[1]:
            # 将数据加入列表
            header.append(column.value)
        return header

    def read_excel(self, sheets_line, line=1):
        """
        从第line行开始，逐行读取，默认第一行是表头，从第二行开始读取
        :param sheets_line:
        :param line:起始行，默认1
        :return:
        """
        sheets_list = sheets_line.split(',')
        data = []  # 最终返回list，给ddt使用
        for sheets in sheets_list:
            sheet = self._open_excel(sheets)  # 打开EXCEL指定sheet页
            headers = self.header_excel(sheets)  # 返回表头
            # 逐行获取数据
            rows = list(sheet.rows)
            for row in rows[line:]:
                row_cell = []
                for cell in row:
                    row_cell.append(cell.value)  # 获取同一行每个单元格数据
                data_dict = dict(zip(headers, row_cell))  # 返回每行数据，格式为{'表头'：'单元格内容'})
                data.append(data_dict)  # list有序
        self.close_excel()
        return data

    def write_excel(self, sheet_name, row, column, data):
        """
        写Excel
        :param sheet_name: Excel页签
        :param row: 行号
        :param column: 列号
        :param data:写入的数据
        :return:空
        """
        sheet = self._open_excel(sheet_name)
        sheet.cell(row, column).value = data
        self.close_excel()

    def close_excel(self):
        """关闭"""
        self.wb.save(self.file)
        self.wb.close()


if __name__ == '__main__':
    pass
