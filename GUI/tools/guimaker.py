"""
自动化生成菜单和工具栏.有GUIMaker(GuiMakerFrameMenu)类和GuiMakerWindowMenu类.子类需要start方法根据布局树格式定制菜单menuBar列表和工具栏toolBar列表(`__name__`测试示例),help方法定制帮助选项,makeWidgets方法定制中间内容
"""

import sys
from tkinter import *                    
from tkinter.messagebox import showinfo

class GuiMaker(Frame):
    """
    用于嵌入式组件菜单和工具栏
    """
    
    menuBar    = []                     
    toolBar    = []                      
    helpButton = True                     

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)       
        self.start()                           
        self.makeMenuBar()                      
        self.makeToolBar()                    
        self.makeWidgets()                      

    def makeMenuBar(self):
        """
        创建自定义菜单栏和帮助按钮
        """
        
        menubar = Frame(self, relief=RAISED, bd=2)
        menubar.pack(side=TOP, fill=X)

        for (name, key, items) in self.menuBar:
            mbutton  = Menubutton(menubar, text=name, underline=key)
            mbutton.pack(side=LEFT)
            pulldown = Menu(mbutton)
            self.addMenuItems(pulldown, items)
            mbutton.config(menu=pulldown)

        if self.helpButton:
            Button(menubar, text    = 'Help',
                            cursor  = 'gumby',
                            relief  = FLAT,
                            command = self.help).pack(side=RIGHT)

    def addMenuItems(self, menu, items):
        """
        列表中每一项代表一个menu,传递名称,快捷键和回调函数的三元组,当menu是子菜单时,将回调函数换为嵌套列表.也可以在列表中传入separator字符串添加分割线或不可用menu的索引(从一开始,separator也算)列表或标签.
        """
        
        for item in items:                     
            if item == 'separator':            
                menu.add_separator({})
            elif type(item) == list:           
                for num in item:
                    menu.entryconfig(num, state=DISABLED)  # 查询和更改菜单项目选项
            elif type(item[2]) != list:
                menu.add_command(label     = item[0],         
                                 underline = item[1],         
                                 command   = item[2])         
            else:
                pullover = Menu(menu)
                self.addMenuItems(pullover, item[2])          
                menu.add_cascade(label     = item[0],         
                                 underline = item[1],         
                                 menu      = pullover)

    def makeToolBar(self):
        """
        创建工具栏,列表中每一项是一个名称,回调函数,pack选项字典的三元组   
        """
        
        if self.toolBar:
            toolbar = Frame(self, cursor='hand2', relief=SUNKEN, bd=2)
            toolbar.pack(side=BOTTOM, fill=X)
            for (name, action, where) in self.toolBar:
                Button(toolbar, text=name, command=action).pack(where)

    def makeWidgets(self):
        """
        中间内容,可扩展默认,由子类定制.
        """
        name = Label(self,
                     width=40, height=10,
                     relief=SUNKEN, bg='white',
                     text   = self.__class__.__name__,
                     cursor = 'crosshair')
        name.pack(expand=YES, fill=BOTH, side=TOP)

    def help(self):
        """
        帮助选项,子类定制
        """
        
        showinfo('Help', 'Sorry, no help for ' + self.__class__.__name__)

    def start(self):
        """
        根据布局树格式设置菜单和工具栏,子类定制
        """ 
        
        self.menuBar = menuBar
        self.toolBar = toolBar

GuiMakerFrameMenu = GuiMaker          

class GuiMakerWindowMenu(GuiMaker):  
    """
    用于顶层窗口菜单.只是对GUImaker的定制子类
    """
      
    def makeMenuBar(self):
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        for (name, key, items) in self.menuBar:
            pulldown = Menu(menubar)
            self.addMenuItems(pulldown, items)
            menubar.add_cascade(label=name, underline=key, menu=pulldown)

        if self.helpButton:
            if sys.platform[:3] == 'win':
                menubar.add_command(label='Help', command=self.help)
            else:
                pulldown = Menu(menubar)  
                pulldown.add_command(label='About', command=self.help)
                menubar.add_cascade(label='Help', menu=pulldown)




if __name__ == '__main__':
    from guimixin import GuiMixin            

    menuBar = [
        ('File', 0,
            [('Open',  0, lambda:0),         
             ('Quit',  0, sys.exit)]),       
        ('Edit', 0,
            [('Cut',   0, lambda:0),
             ('Paste', 0, lambda:0)]) ]
    toolBar = [('Quit', sys.exit, {'side': LEFT})]

    class TestAppFrameMenu(GuiMixin, GuiMakerFrameMenu):
        def start(self):
            self.menuBar = menuBar
            self.toolBar = toolBar

    class TestAppWindowMenu(GuiMixin, GuiMakerWindowMenu):
        def start(self):
            self.menuBar = menuBar
            self.toolBar = toolBar

    class TestAppWindowMenuBasic(GuiMakerWindowMenu):
        def start(self):
            self.menuBar = menuBar
            self.toolBar = toolBar    

    root = Tk()
    TestAppFrameMenu(Toplevel())
    TestAppWindowMenu(Toplevel())
    TestAppWindowMenuBasic(root)
    root.mainloop()
