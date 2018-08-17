## rename:

批量修改文件名

使用:`python rename dir_path rm_key `
将dir_path目录下所有文件名中删除rm_key    
    
## split_join_file:

分割和合并文件,分割函数split_f将大文件分割为小文件,合并函数join_f将分割后的小文件重新拼回大文件
split_f(from_file, to_dir, part_size=part_size):拆分文件 
join_f(from_dir, to_file):合并文件

使用:`python split_join_file.py filename|dirpath [dirpath|filename]  [partsize]`
    
## bigpy:

递归扫描指定目录,找到特定的文件扩展名(默认当前目录,.py文件,跟踪目录)

使用:`python bigpy.py [dir]  [extename]  [0|1|2]`

## cpall:

复制目录树,跳过出错文件,继续复制.

使用:`python cpall.py form_dir to_dir`

## diffall:

递归的比较两个目录,打印出双方特有的,和共同所有的相异的

使用:`python diffall.py diff_dir1 diff_dir2`

## zipall:

将指定目录下所有的文件分别压缩,放入指定目录.最后压缩后文件中会包含祖先目录文件夹

使用:`python zipall.py file_dir `

## maohao_to_dirc.py:

文本格式化转换,并提供将其持久化的导入导出功能.将 (键:值/n 键:值/n)类型文本转化为字典对象

使用:导入to_dir('文件路径名')方法:返回字典对象.需要有原始文件

## to_table.py

将符号分割文本转化为markdown表格形式

使用:`python to_table filename rept`filename是文件名,默认test,rept是文件分割符号,默认' '.需要有原始文件.

## autopep8all.py

遍历一个目录,将该目录下所有的.py文件用autopep8规范化

使用: `python autopep8all.py dirname [recursion=False]`


