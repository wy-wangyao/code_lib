#! /usr/bin/env python

"""
基于队列的消费者/生成者多线程GUI.提供将一个模态操作分解为线程和后线程步骤.`__name__`测试中示例用法.定义相关的回调函数,线程功能,初始化线程函数参数等.
"""

try:  # 当thread模块不存在时,使可用
    import _thread as thread
except ImportError:
    import _dummy_thread as thread

import queue
import sys
threadQueue = queue.Queue(maxsize=0)


def threadChecker(widget, delayMsecs=100, perEvent=1):
    """
    周期性的检查队列,从队列中取出回调函数执行.参数分别是周期间隔和一个周期处理函数的个数,多了可能阻塞界面,少了耗时.
    """

    for i in range(perEvent):
        try:
            (callback, args) = threadQueue.get(block=False)
        except queue.Empty:
            break
        else:
            callback(*args)
    widget.after(delayMsecs,
                 lambda: threadChecker(widget, delayMsecs, perEvent))


def threaded(action, args, context, onExit, onFail, onProgress):
    """
    线程调用函数,参数分别是(主要功能函数,参数,识别每个线程,退出回调函数,失败回调函数,正常运行回调函数).调用线程的主要功能,将回调函数加入队列.
    """

    try:
        if not onProgress:
            action(*args)
        else:
            def progress(*any):
                threadQueue.put((onProgress, any + context))
            action(progress=progress, *args)
    except BaseException:
        threadQueue.put((onFail, (sys.exc_info(), ) + context))
    else:
        threadQueue.put((onExit, context))


def startThread(action, args, context, onExit, onFail, onProgress=None):
    """
    生成线程
    """

    thread.start_new_thread(
        threaded, (action, args, context, onExit, onFail, onProgress))


class ThreadCounter:
    """
    线程安全的计数器,当线程更新其他不是不是由线程回调队列管理的共享状态时,可避免操作重叠.
    """

    def __init__(self):
        self.count = 0
        self.mutex = thread.allocate_lock()

    def incr(self):
        self.mutex.acquire()
        self.count += 1
        self.mutex.release()

    def decr(self):
        self.mutex.acquire()
        self.count -= 1
        self.mutex.release()

    def __len__(self): return self.count


if __name__ == '__main__':
    import time
    from tkinter.scrolledtext import ScrolledText

    def onEvent(i):
        """
        初始化线程函数参数,调用线程生成函数
        """

        myname = 'thread-%s' % i
        startThread(
            action=threadaction,
            args=(i, 3),
            context=(myname,),
            onExit=threadexit,
            onFail=threadfail,
            onProgress=threadprogress)

    def threadaction(id, reps, progress):
        """
        线程的主要功能,在新的线程中运行.这里是生产自定义数量个回调函数,并手动制作一些运行异常的函数
        """

        for i in range(reps):
            time.sleep(1)
            if progress:
                progress(i)   # 将回调函数加入队列
        if id % 2 == 1:
            raise Exception

    def threadexit(myname):
        """
        退出的回调函数
        """

        text.insert('end', '%s\texit\n' % myname)
        text.see('end')

    def threadfail(exc_info, myname):
        """
        运行失败的回调函数
        """

        text.insert('end', '%s\tfail\t%s\n' % (myname, exc_info[0]))
        text.see('end')

    def threadprogress(count, myname):
        """
        正常运行的回调函数
        """

        text.insert('end', '%s\tprog\t%s\n' % (myname, count))
        text.see('end')
        text.update()

    text = ScrolledText()
    text.pack()
    threadChecker(text)
    text.bind('<Button-1>',
              lambda event: list(map(onEvent, range(6))))
    text.mainloop()
