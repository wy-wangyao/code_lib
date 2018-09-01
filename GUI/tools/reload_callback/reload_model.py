"""
实际运行的函数,每次触发都重新加载.传入self参数可访问实例
"""

def message1():                 
    print('spamSpamSPAM')      

def message2(self):
    print('Ni! Ni!')           
    self.method1() 
