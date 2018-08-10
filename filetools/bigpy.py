"""
递归扫描指定目录,找到特定的文件扩展名,默认为当前目录下的pyhon文件,可以有三个可选的参数依次是目录名,文件扩展名,跟踪级别(0:无,1:目录,2:文件)

是否真的有必要避免同一目录扫描两次存疑,似乎不会出现这种情况
"""
#import pdb
import os, pprint
from sys import argv, exc_info
#pdb.set_trace()
dirname, extname, trace = os.curdir, '.py', 1
if len(argv) > 1:
    dirname = argv[1]
if len(argv) > 2:
    extname = argv[2]
if len(argv) > 3:
    trace = int(argv[3])  # 一时疏忽,忘记转化为整型,调试了半天


def tryprint(arg):
    try:
        print(arg)
    except UnicodeEncodeError:
        print(arg.encode())


visited = set()
allsizes = []
for (thisdir, subsHere, filesHere) in os.walk(dirname):
    if trace:tryprint(thisdir)
    thisdir = os.path.normpath(thisdir)
    fixname = os.path.normcase(thisdir)
    if fixname in visited:  # 避免重复扫描
        if trace:tryprint('skipping' + thisdir)
    else:
        visited.add(fixname)
        for filename in filesHere:
            if filename.endswith(extname):
                if trace > 1:tryprint('+++' + filename)
                fullname = os.path.join(thisdir, filename)
                try:
                    bytesize = os.path.getsize(fullname)
                    linesize = sum(1 for line in open(fullname, 'rb'))
                except Exception:
                    print('error', exc_info()[0])
                else:
                    allsizes.append((bytesize, linesize, fullname))

for (title, key) in [('bytes', 0), ('lines', 1)]:
    print('\nBy %s...' % title)
    allsizes.sort(key=lambda x: x[key])
    pprint.pprint(allsizes[:3])
    pprint.pprint(allsizes[-3:])

