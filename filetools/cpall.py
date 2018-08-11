"""
复制目录树,跳过出错文件,继续复制
"""

import os, sys, time
import pdb

maxsize = 1024 * 1024 * 10
partsize = 1024 * 1024 *5

def cpfile(fromfile, tofile, maxsize=maxsize):
    """
    复制文件

    Args:
        fromfile: 原文件
        tofile: 目标文件
        maxsize: 直接复制,单个文件最大字节数

    """

    if os.path.getsize(fromfile) <  maxsize:
        bytesfrom = open(fromfile, 'rb').read()
        with open(tofile, 'wb') as f:
            f.write(bytesfrom)
    else:
        file_from = open(fromfile, 'rb')
        file_to = open(tofile, 'wb')
        while True:
            bytesfrom = file_from.read(partsize)
            if not bytesfrom:
                break
            file_to.write(bytesfrom)
        file_to.close()


def cp_tree(fromdir, todir, verbose=0):
    """
    复制目录树

    Args:
        fromdir: 原目录
        todir: 目标目录
        verbose: 跟踪级别,0:不跟踪,1:跟踪目录,2:跟踪文件

    Return:
        (fcount, dcount):复制的文件数和目录数

    """

    fcount = dcount = 0
    for filename in os.listdir(fromdir):
        pathfrom = os.path.join(fromdir, filename)
        pathto = os.path.join(todir, filename)
        if  not os.path.isdir(pathfrom):
            try:
                if verbose > 1:
                    print('copying', pathfrom, 'to', pathto)
                cpfile(pathfrom, pathto)
                fcount += 1
            except Exception:
                print('Error coping', pathfrom, 'to', pathto)
        else:
            if verbose >0:
                print('coping', pathfrom, 'to', pathto)
            try:
                os.mkdir(pathto)
                below = cp_tree(pathfrom, pathto)
                fcount += below[0]
                dcount += below[1]
                dcount += 1
            except Exception:
                print('Error creating', pathto, '--skipped')
                print(sys.exc_info()[0], sys.exc_info()[1])
    return (fcount, dcount)

def getargs():
    """
    获取并验证文件目录名参数,验证包括:原目录合法验证,目标目录存在验证,目标目录位于原目录下验证,原目录与目标目录相同验证

    Return:
        (fromdir,todir):原目录,目标目录
    """

    try:
        fromdir, todir = sys.argv[1:]
    except Exception:
        print('Usage error: python cpall.py fromdir todir')
    else:
        assert (fromdir not in todir), 'todir in fromdir, change todir '
        if not os.path.isdir(fromdir):
            print('Error: fromdir is not a directory')
        elif not os.path.exists(todir):
            os.mkdir(todir)
            print('Note: todir was created')
            return (fromdir, todir)
        else:
            print('waring:directory already exists')
            if hasattr(os.path, 'samefile'):
                same = os.path.samefile(fromdir, todir)
            else:
                same = os.path.abspath(fromdir) == os.path.abspath(todir)
            if same:
                print('Error:fromdir same as todir')
            else:
                return (fromdir, todir)


if __name__ == '__main__':
    pdb.set_trace()
    dirstuple = getargs()
    if dirstuple:
        print('copying...')
        start = time.clock()
        fcount, dcount = cp_tree(*dirstuple)
        print('copy', fcount, 'file,', dcount, 'directory', end='')
        print('in', time.clock() - start, 'seconds')


