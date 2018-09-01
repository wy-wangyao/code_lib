"""
类库.ShellGui作为父类,无法产生实例.LIstMenuGui和DictMenuGui是其子类,分别以列表和字典方式提供工具名称列表.实现的子类(name测试示例)需要以相应的方式初始化myMenu工具名称列表,可选的重写forToolBar方法,放置在工具栏的工具名称传入后返回True.

依赖于guimaker(强依赖)和guimixin(弱依赖)
"""

from tkinter import *
from guimixin import GuiMixin
from guimaker import *


class ShellGui(GuiMixin, GuiMakerWindowMenu):
    def start(self):
        self.setMenuBar()
        self.setToolBar()
        self.master.title("Shell Tools Listbox")
        self.master.iconname("Shell Tools")

    def handleList(self, event):
        """
        根据点击名称,运行工具动作
        """

        label = self.listbox.get(ACTIVE)
        self.runCommand(label)

    def makeWidgets(self):
        """
        布局中间内容,以列表框的方式显示每一个工具
        """

        sbar = Scrollbar(self)
        list = Listbox(self, bg='white')
        sbar.config(command=list.yview)
        list.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        list.pack(side=LEFT, expand=YES, fill=BOTH)
        for (label, action) in self.fetchCommands():
            list.insert(END, label)
        list.bind('<Double-1>', self.handleList)
        self.listbox = list

    def forToolBar(self, label):
        """
        设置放到工具栏上的工具
        """

        return True

    def setToolBar(self):
        """
        设置工具栏
        """

        self.toolBar = []
        for (label, action) in self.fetchCommands():
            if self.forToolBar(label):
                self.toolBar.append((label, action, dict(side=LEFT)))
        self.toolBar.append(('Quit', self.quit, dict(side=RIGHT)))

    def setMenuBar(self):
        """
        设置菜单
        """

        toolEntries = []
        self.menuBar = [
            ('File', 0, [('Quit', -1, self.quit)]),
            ('Tools', 0, toolEntries)
        ]
        for (label, action) in self.fetchCommands():
            toolEntries.append((label, -1, action))

    def fetchCommands(self):
        """
        函数声明,不是必须,不是很pythonic,但更加友好.

        方法的作用是提供工具集列表
        """

        raise NotImplementedError()

    def runCommand(self, cmd):
        """
        按名称分派动作
        """

        raise NotImplementedError()


class ListMenuGui(ShellGui):
    """
    列表[(label, callback)]布局的工具集列表
    """

    def fetchCommands(self):
        return self.myMenu

    def runCommand(self, cmd):
        for (label, action) in self.myMenu:
            if label == cmd:
                action()


class DictMenuGui(ShellGui):
    """
    字典{{label: callback}}布局的工具集列表
    """

    def fetchCommands(self):
        return self.myMenu.items()

    def runCommand(self, cmd):
        self.myMenu[cmd]()


if __name__ == "__main__":
    import os

    class Demo(ListMenuGui):
        def __init__(self):
            self.myMenu = [('Quit', self.quit),
                           ('Dir', os.getcwd)]
            ListMenuGui.__init__(self)

        def forToolBar(self, label):
            return label in {'Dir'}
    Demo().mainloop()
