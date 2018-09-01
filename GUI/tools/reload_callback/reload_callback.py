"""
动态重载回调函数示例,在回调函数中重载模块,调用模块中实际运行可动态修改的函数.
"""

from tkinter import *
import reload_model           
from imp import reload      

class Hello(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.make_widgets()

    def make_widgets(self):
        Button(self, text='message1', command=self.message1).pack(side=LEFT)
        Button(self, text='message2', command=self.message2).pack(side=RIGHT)

    def message1(self):
        reload(radactions)         
        radactions.message1()      

    def message2(self):
        reload(radactions)         
        radactions.message2(self)  

    def method1(self):
        print('exposed method...')       

Hello().mainloop()
