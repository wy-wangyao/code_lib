"""
文件处理类DealFile,初始化需要传入文件名.no_annotation方法去除py中的#号注释.用法python dealfile.py <filename>
"""

import os
import sys


class DealFile:
    """
    文件处理类,初始化需要传入文件名
    """

    def __init__(self, filename, *args):
        self.filename = filename

    def no_annotation(self):
        """
        去除py中的#号注释
        """

        ow = True
        tw = True
        infile = open(self.filename, 'r')
        outfile = open(self.filename + '.new.py', 'w')
        for line in infile:
            for char in line:
                if char == '"':
                    tw = not tw
                if char == "'":
                    ow = not ow
                if tw and ow and char == '#':
                    outfile.write(os.linesep)
                    break
                outfile.write(char)
        infile.close()
        outfile.close()
        os.rename(self.filename, self.filename + '.old.py')
        os.rename(self.filename + '.new.py', self.filename)


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except Exception:
        print("Erorr:", exce_info())
    df = DealFile(filename)
    df.no_annotation()
