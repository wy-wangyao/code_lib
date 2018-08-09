"""
分割和合并文件,分割函数split_f将大文件分割为小文件,合并函数join_f将分割后的小文件重新拼回大文件.

命令行运行:python split_join_file.py from_path [to_path] [part_size]
默认只需要给出要拆分的文件的路径,自动创建文件夹,合并时也只用指定要合并的文件夹即可

可以自己指定拆分到的文件夹路径,但和并的时候也要自己指定合并到的文件路径

可以指定拆分时的每一个拆分文件大小,以1MB为单位,默认10MB
"""

import os
import sys
import pdb

base_size = 1024 * 1024
part_size = 10


def split_f(from_file, to_dir, part_size=part_size):
    '''
    拆分文件

    Args:
        from_file: 原文件路径
        to_dir: 目标文件夹路径
        part_size: 每一个拆分文件的大小
    '''

    if not os.path.exists(to_dir):
        os.mkdir(to_dir)
    else:
        for fname in os.listdir(to_dir):
            os.remove(os.path.join(to_dir, fname))
    partnum = 0
    file_data = open(from_file, 'rb')
    while True:
        chunk = file_data.read(part_size * base_size)
        if not chunk:
            break
        partnum += 1
        from_name = from_file.split(os.sep)[-1]
        filename = os.path.join(to_dir, ('part%04d_%s' % (partnum, from_name)))
        fileobj = open(filename, 'wb')
        fileobj.write(chunk)
        fileobj.close()
    file_data.close()
    assert partnum <= 9999
    return partnum


def join_f(from_dir, to_file):
    '''
    合并文件

    Args:
        from_dir: 原小文件目录
        to_file:合并到目标文件名
    '''

    parts = sorted(os.listdir(from_dir))
    fileobj = open(to_file, 'wb')
    for part in parts:
        filepath = os.path.join(from_dir, part)
        partdata = open(filepath, 'rb').read()
        fileobj.write(partdata)
    fileobj.close()


if __name__ == '__main__':
    pdb.set_trace()
    try:
        if len(sys.argv) == 2:
            from_path = sys.argv[1]
            from_path = os.path.abspath(from_path)
            if os.path.isfile(from_path):
                split_f(from_path, from_path + '_dir')
            if os.path.isdir(from_path):
                filename = from_path[:-4]
                join_f(from_path, filename)
        if len(sys.argv) > 2:
            from_path = sys.argv[1]
            to_path = sys.argv[2]
            if len(sys.argv) > 3:
                part_size = sys.argv[3]
            if os.path.isfile(from_path):
                split_f(from_path, to_path, part_size)
            else:
                join_f(from_path, to_path)
    except Exception:
        print('Error', sys.exc_info()[0])
