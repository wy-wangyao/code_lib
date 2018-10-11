"""
文件处理类DealFile,初始化需要传入文件名.no_annotation方法去除py中的#号注释.用法python dealfile.py <filename>
"""

import os
import sys


class DealFile:
    """
    文件处理类,初始化需要传入文件名
    """

    def no_annotation(self, filename):
        """
        去除py中的#号注释
        """

        ow = True
        tw = True
        infile = open(filename, 'r')
        outfile = open(filename + '.new.py', 'w')
        for line in infile:
            for char in line:
                if char == '"' and ow:
                    tw = not tw
                if char == "'" and tw:
                    ow = not ow
                if tw and ow and char == '#':
                    outfile.write(os.linesep)
                    break
                outfile.write(char)
        infile.close()
        outfile.close()
        os.rename(filename, filename + '.old.py')
        os.rename(filename + '.new.py', filename)


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except Exception:
        print("Erorr:", exce_info())
    df = DealFile()
    df.no_annotation(filename)
