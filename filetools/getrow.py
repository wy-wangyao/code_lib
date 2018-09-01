"""
获取文件行数或某些文件的总行数的类GetRow.有get_pyfile_row(python文件统计)方法和get_dir_row(多个文件统计,通过实现并指定func可以统计其他文件)方法.暂时有个漏洞,文本注释结尾三引号后出现一对另一种文本注释三引号,会忽略后面.
"""

import os
import sys
import glob
import pdb


class GetRow:
    def __init__(self):
        self.model = '*.py'
        self.trace = True
        
    def get_pyfile_row(self, filename):
        """
        获得py文件的行数.忽略注释和空行
        """

        fileobj = open(filename, 'r')
        rows = 0
        swd = True
        sws = True
        for row in fileobj:
            if not row.strip() or row.lstrip().startswith('#'):
                continue
            if row.strip().startswith('"""') and sws and swd or '= """' in row:
                swd = not swd
            elif row.strip().endswith('"""') and sws and not swd:
                rows -= 1
                swd = not swd
            if row.strip().startswith("'''") and swd and sws or "= '''" in row:
                sws = not sws
            elif row.strip().endswith("'''") and swd and not sws:
                rows -= 1
                sws = not sws
            if swd and sws:
                rows += 1
        if self.trace:
            print(filename, '>>>', rows)
        return rows

    def get_filemodel_row(
            self,
            dirname='./',
            get_file_row=get_pyfile_row):
        """
        获取某目录下,文件名匹配相应模式的文件的行数,默认当前目录下的.py结尾的文件.
        """

        rows = 0
        filemodel = os.path.join(dirname, self.model)
        for filename in glob.glob(filemodel):
            row = get_file_row(self, filename)
            rows += row
        return rows
        
    def setmodel(self, model):
        """
        选取的文件,支持*,?等
        """
        
        self.model = model
        
    def settrace(self, trace):
        """
        是否跟踪每个文件的行数
        """
        
        self.trace = trace


if __name__ == '__main__':
    pdb.set_trace()
    try:
        getrow = GetRow()
        args = sys.argv[1:]
        rows = getrow.get_filemodel_row(*args)    
    except Exception:
        print('ArgvEroor: try: python getrow.py [dirorfile]')
    print(rows)
