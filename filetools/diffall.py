"""
比较两个目录,找出其中的差异
"""

import os
import sys

partsize = 1024 * 1024


def getargs():
    """
    获取命令行参数

    Return:
        (diff_dir1,diff_dir2): 要比较的两个目录
    """

    try:
        diff_dir1, diff_dir2 = sys.argv[1:]
    except Exception:
        print(sys.exc_info()[0], 'Usage:python diffall.py diff1 diff2')
        sys.exit(1)
    else:
        return (diff_dir1, diff_dir2)


def compare(diff_dir1, diff_dir2):
    """
    递归的比较两个目录,打印出双方特有的,和共同所有的相异的

    Args:
        (diff_dir1,diff_dir2): 要比较的两个目录
    """

    subfiles1 = os.listdir(diff_dir1)
    subfiles2 = os.listdir(diff_dir2)
    diffs1 = getdiff(subfiles1, subfiles2)
    diffs2 = getdiff(subfiles2, subfiles1)
    common = [item for item in subfiles1 if item in subfiles2]
    printdiff(diff_dir1, diffs1)
    printdiff(diff_dir2, diffs2)
    subtypes = gettype(diff_dir1, diff_dir2, common)
    list(map(compare, subtypes[0], subtypes[1]))
    list(map(comtext, subtypes[2], subtypes[3]))


def comtext(filename1, filename2, partsize=partsize):
    """
    比较同名文件的内容是否相同.

    Args:
        filename1,filename2: 两个同名文件
        partsize: 比较时读取文件块的大小
    """

    file1 = open(filename1, 'rb')
    file2 = open(filename2, 'rb')
    while True:
        filetext1 = file1.read(partsize)
        filetext2 = file2.read(partsize)
        if filetext1:
            if filetext1 == filetext2:
                pass
            else:
                print('- files differ at', filename1, '-', filename2, '\n')
                break
        else:
            break


def printdiff(diff_dir, diffs):
    """
    打印出双方特有文件

    Args:
        diff_dir: 文件目录
        diffs: 目录下特有文件列表
    """

    for uni in diffs:
        uni = os.path.join(diff_dir, uni)
        print('- unique file at:', uni, '\n')


def gettype(diff_dir1, diff_dir2, common):
    """
    对共有文件进行分类为目录和文件,打印出同名但不同类文件

    Args:
        diff_dir1,diff_dir2: 要比较的两个文件目录
        common: 两个目录共有文件

    Return:
        subdir1:目录1中的子目录
        subdir2:目录2中的子目录
        subfile1:目录1中的子文件
        subfile2:目录2中的子文件
    """

    subfiles1 = []
    subfiles2 = []
    subdirs1 = []
    subdirs2 = []
    for com in common:
        com1 = os.path.join(diff_dir1, com)
        com2 = os.path.join(diff_dir2, com)
        if os.path.isfile(com1) == os.path.isfile(com2):
            if os.path.isfile(com1):
                subfiles1.append(com1)
                subfiles2.append(com2)
            else:
                subdirs1.append(com1)
                subdirs2.append(com2)
        else:
            print('- unique file at:', com1, '\n')
            print('- unique file at:', com2, '\n')
    return (subdirs1, subdirs2, subfiles1, subfiles2)


def getdiff(seq1, seq2):
    """
    找所有出在seq1中存在,在seq2中不存在的项

    Args:
        seq1,seq2:两个不同的序列

    Return:
        unique:seq1中特有的项
    """

    unique = [item for item in seq1 if item not in seq2]
    return unique


if __name__ == '__main__':
    diff_dir1, diff_dir2 = getargs()
    diff_dir1 = os.path.abspath(diff_dir1)
    diff_dir2 = os.path.abspath(diff_dir2)
    compare(diff_dir1, diff_dir2)
