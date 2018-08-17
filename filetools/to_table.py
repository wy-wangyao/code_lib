def to_table(filename='re', rept=' '):
    '''将符号分割文本转化为markdown表格形式

    parameter:需要转化的文件名(str),文本的分割符号(str)
    '''
    file_obj_r = open(filename, 'r')
    file_obj_w = open('new' + filename, 'w')
    count = 0  # 哨兵,实现文件的第二行另做处理
    for line in file_obj_r:
        rec = line.split(rept)
        new_rec = [i.strip() for i in rec]
        new_rec = '|' + '|'.join(new_rec) + '|' + '\n'
        file_obj_w.write(new_rec)
        if count == 0:
            head_rec = '|'
            for i in rec:
                head_rec += '---|'
            head_rec += '\n'
            file_obj_w.write(head_rec)
            count += 1
    file_obj_r.close()
    file_obj_w.close()


if __name__ == '__main__':
    import sys
    try:
        to_table(sys.argv[1], sys.argv[2])
    except BaseException:
        to_table()
