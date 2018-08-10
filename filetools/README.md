rename:批量修改文件名

    rm_name(dirname, rm_key)在指定目录下,递归的查找文件,删除文件名中指定关键字
    
split_join_file:分割和合并文件,分割函数split_f将大文件分割为小文件,合并函数join_f将分割后的小文件重新拼回大文件

    split_f(from_file, to_dir, part_size=part_size):拆分文件
    
    join_f(from_dir, to_file):合并文件
    
bigpy:递归扫描指定目录,找到特定的文件扩展名
