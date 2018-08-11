"""
比较两个目录,找出其中的差异
"""

import os
import sys

partsize = 1024 * 1024


def getargs():
    try:
        diff_dir1, diff_dir2 = sys.argv[1:]
    except Exception:
        print(sys.exc_info()[0], 'Usage:python diffall.py diff1 diff2')
        sys.exit(1)
    else:
        return (diff_dir1, diff_dir2)


def compare(diff_dir1, diff_dir2):
    subfiles1 = os.listdir(diff_dir1)
    subfiles2 = os.listdir(diff_dir2)
    diffs1 = getdiff(subfiles1, subfiles2)
    diffs2 = getdiff(subfiles2, subfiles1)
    common = [item for item in subfiles1 if item in subfiles2]
    subtypes1 = gettype(diff_dir1, diffs1, common)
    subtypes2 = gettype(diff_dir2, diffs2, common)
    list(map(compare, subtypes1[0], subtypes2[0]))
    list(map(comtext, subtypes1[1], subtypes2[1]))


def comtext(filename1, filename2, partsize=partsize):
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


def gettype(diff_dir, diffs, common):
    subfiles = []
    subdirs = []
    for uni in diffs:
        uni = os.path.join(diff_dir, uni)
        print('- unique file at:', uni, '\n')
    for com in common:
        com = os.path.join(diff_dir, com)
        if os.path.isfile(com):
            subfiles.append(com)
        else:
            subdirs.append(com)
    return (subdirs, subfiles)


def getdiff(seq1, seq2):
    unique = [item for item in seq1 if item not in seq2]
    return unique


if __name__ == '__main__':
    diff_dir1, diff_dir2 = getargs()
    diff_dir1 = os.path.abspath(diff_dir1)
    diff_dir2 = os.path.abspath(diff_dir2)
    compare(diff_dir1, diff_dir2)
