"""
给定一个目录,将该目录下所有的.py文件用autopep8规范化
"""
import os
import sys


def autopep8all(dirname, recursion=True):
    """
    遍历一个目录,将该目录下所有的.py文件用autopep8规范化
    """
    if recursion:
        for (filename, filepath) in get_recursion_filename_iter(dirname):
            autopep8file(filename)
    else:
        for filename in get_filename_iter(dirname, dirname=False):
            autopep8file(filename)


def autopep8file(filename):
    """
    判断文件是否为.py,如果是就规范化
    """

    if filename.endswith('.py'):
        os.system(
            'autopep8 --in-place --aggressive --aggressive %s' %
            filename)


def get_recursion_filename_iter(dirname):
    """
    递归的返回目录下的文件名和路径
    """
    curdir = os.curdir
    for (thisdir, subdir, subfile) in os.walk(dirname):
        os.chdir(thisdir)
        for filename in subfile:
            yield (filename, os.path.join(thisdir, filename))
        os.chdir(curdir)


def get_filename_iter(dirname, have_dir=True):
    """
    返回目录下的文件名,默认包括目录,当dirname为False时,只返回文件名
    """

    for fileanme in os.listdir(dirname):
        if os.path.isfile(filename):
            yield filename
        if os.path.isdir(filename) and have_dir:
            yield filename


if __name__ == '__main__':
    try:
        dirname = sys.argv[1]
        recursion = True
        if len(sys.argv) == 3:
            recursion = sys.argv[2]
        autopep8all(dirname, recursion=recursion)
    except Exception:
        print('try: python autopep8all.py dirname')
