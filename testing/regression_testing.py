"""
回归测试脚本,命令行传入测试目录(默认当前目录)测试目录下有Scripts目录:存放待测试脚本,Input目录:存放与脚本同名,以.in为后缀的输入文件,Args目录:存放以.args为后缀的参数文件,Output目录存放以.out为后缀的输出文件和out.bad为后缀的错误输出文件,Error目录存放以.err为后缀的错误文件
"""

import os
import sys
import glob
import time
from subprocess import Popen, PIPE

# configuration args
testdir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
forcegen = len(sys.argv) > 2
print('Start tester:', time.asctime())
print('in', os.path.abspath(testdir))


def verbose(*args):
    print('-' * 80)
    for arg in args:
        print(arg)


def quiet(*args): pass


trace = quiet  # 控制是否追踪,trace = verbose时追踪

# 获取待测试脚本
testpatt = os.path.join(testdir, 'Scripts', '*.py')
testfiles = sorted(glob.glob(testpatt))
trace(os.getcwd(), *testfiles)

numfail = 0  # 记录错误测试
for testpath in testfiles:
    testname = os.path.basename(testpath)

    # 获取输入和参数文件
    infile = testname.replace('.py', '.in')
    inpath = os.path.join(testdir, 'Inputs', infile)
    indata = open(inpath, 'rb').read() if os.path.exists(inpath) else b''

    argfile = testname.replace('.py', '.args')
    argpath = os.path.join(testdir, 'Args', argfile)
    argdata = open(argpath).read() if os.path.exists(argpath) else ''

    # 定位输出和错误,清除前次结果
    outfile = testname.replace('.py', '.out')
    outpath = os.path.join(testdir, 'Outputs', outfile)
    outpathbad = outpath + '.bad'
    if os.path.exists(outpathbad):
        os.remove(outpathbad)

    errfile = testname.replace('.py', '.err')
    errpath = os.path.join(testdir, 'Errors', errfile)
    if os.path.exists(errpath):
        os.remove(errpath)

    # 进行测试,获取标准流
    pypath = sys.executable
    command = '%s %s %s' % (pypath, testpath, argdata)
    trace(command, indata)

    process = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    process.stdin.write(indata)
    process.stdin.close()
    outdata = process.stdout.read()
    errdata = process.stderr.read()
    exitstatus = process.wait()
    trace(outdata, errdata, exitstatus)

    # 分析结果
    if exitstatus != 0:
        print('ERROR status:', testname, exitstatus)
    if errdata:
        print('ERROR stream:', testname, errpath)
        open(errpath, 'wb').write(errdata)

    if exitstatus or errdata:
        numfail += 1
        open(outpathbad, 'wb').write(outdata)

    elif not os.path.exists(outpath) or forcegen:
        print('generating:', outpath)
        open(outpath, 'wb').write(outdata)

    else:
        priorout = open(outpath, 'rb').read()
        if priorout == outdata:
            print('passed:', testname)
        else:
            numfail += 1
            print('FAILED output:', testname, outpathbad)
            open(outpathbad, 'wb').write(outdata)

print('Finished:', time.asctime())
print('%s tests were run, %s tests failed.' % (len(testfiles), numfail))
