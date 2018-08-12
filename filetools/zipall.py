"""
将指定目录下所有的文件分别压缩,放入指定目录.最后压缩后文件中会包含祖先目录文件夹.
"""

import os
import sys
import zipfile
# import pdb


def getargs():
    """
    获取命令行参数
    """

    try:
        file_dir, zip_dir = sys.argv[1:]
    except Exception:
        print('Error,Usage:python zipall.py file_dir zip_dir')
        sys.exit(1)
    else:
        return (file_dir, zip_dir)


def getfile(file_dir):
    """
    获取文件目录下所有文件(包括子目录)

    Args:
        file_dir: 文件目录

    Return:
        file_list: 包含文件路径和文件名的二元祖列表
    """

    file_list = []
    try:
        for (thisdir, subdirs, subfiles) in os.walk(file_dir):
            for filename in subfiles:
                filepath = os.path.join(thisdir, filename)
                file_list.append((filepath, filename))
    except Exception:
        print(sys.exc_info()[0], sys.exc_info()[1])
    else:
        return file_list


def getzip(file_list, zip_dir):
    """
    生成压缩包

    Args:
        file_list: 包含文件路径和文件名的元祖列表
        zip_dir: 压缩包存放目录
    """

    if not os.path.exists(zip_dir):
        os.mkdir(zip_dir)
    for (filepath, filename) in file_list:
        try:
            zippath = os.path.join(zip_dir, filename + '.zip')
            zipobj = zipfile.ZipFile(zippath, 'w')
            zipobj.write(filepath)
            zipobj.close()
        except Exception:
            print('Error:', sys.exc_info()[0])


# pdb.set_trace()
if __name__ == '__main__':
    file_dir, zip_dir = getargs()
    file_list = getfile(file_dir)
    getzip(file_list, zip_dir)
