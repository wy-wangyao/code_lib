"""
可复用的mixin类,预制了对话框,生成程序,简易文本查看器等方法.作为其他类的父类,为其子类提供功能.name测试可作为用法示例.
"""

import os
import sys
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.scrolledtext import ScrolledText

class GuiMixin:
    def infobox(self, title, text, *args):              
        return showinfo(title, text)                    

    def errorbox(self, text):
        showerror('Error!', text)

    def question(self, title, text, *args):
        return askyesno(title, text)                    

    def notdone(self):
        showerror('Not implemented', 'Option not available')

    def quit(self):
        ans = self.question('Verify quit', 'Are you sure you want to quit?')
        if ans:
            Frame.quit(self)                            

    def help(self):
        """
        建议根据子类的不同,做不同的重写
        """
        
        self.infobox('RTFM', 'See figure 1...')         

    def selectOpenFile(self, file="", dir="."):         
        return askopenfilename(initialdir=dir, initialfile=file)

    def selectSaveFile(self, file="", dir="."):
        return asksaveasfilename(initialfile=file, initialdir=dir)

    def clone(self, args=()):
        """
        打开一个新的独立副本
        """
                      
        new = Toplevel()                   
        myclass = self.__class__           
        myclass(new, *args)                

    def spawn(self, pycmdline, wait=False):
        """
        启动一个新的python独立进程
        """
        
        if not wait:
            os.spawnv(os.P_NOWAIT, sys.executable, ('python', pycmdline)) # 完全独立
        else:
            os.system('%s %s' % (sys.executable, pycmdline)) # 会阻塞GUI
    
    def browser(self, filename):
        """
        生成一个简易文本编辑器
        """
                                
        new  = Toplevel()                                
        text = ScrolledText(new, height=30, width=85)    
        text.config(font=('courier', 10, 'normal'))      
        text.pack(expand=YES, fill=BOTH)
        new.title("Text Viewer")                         
        new.iconname("browser")
        text.insert('0.0', open(filename, 'r').read() )  
    

if __name__ == '__main__':

    class TestMixin(GuiMixin, Frame):      
        def __init__(self, parent=None):
            Frame.__init__(self, parent)
            self.pack()
            Button(self, text='quit',  command=self.quit).pack(fill=X)
            Button(self, text='help',  command=self.help).pack(fill=X)
            Button(self, text='clone', command=self.clone).pack(fill=X)
            Button(self, text='spawn', command=self.other).pack(fill=X)
        def other(self):
            self.spawn('guimixin.py')  
    TestMixin().mainloop()
