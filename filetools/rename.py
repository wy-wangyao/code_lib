"""
批量修改文件名
"""

import os
import sys


def rm_name(dirname, rm_key):
    '''
    在指定目录下,递归的查找文件,删除文件名中指定关键字

    Args:
        dirname: 目录名
        rm_key: 需要删除的关键字

    Return:
        成功返回0,失败返回错误信息
    '''

    for (thisdir, subsdir, filelist) in os.walk(dirname):
        for filename in filelist:
            if rm_key in filename:
                try:
                    new_name = filename.replace(rm_key, '')
                    os.rename(filename, new_name)
                except Exception:
                    print('RenameError', sys.exc_info()[0])


if __name__ == '__main__':
    try:
        dirname = sys.argv[1]
        rm_key = sys.argv[2]
        rm_name(dirname, rm_key)
    except Exception:
        print('ArgvError', sys.exc_info()[0])
