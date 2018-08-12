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


