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
