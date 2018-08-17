'''
文本格式化转换,并提供将其持久化的导入导出功能.将 (键:值/n 键:值/n)类型文本转化为字典对象
'''

import pickle


def process_filename(filename):
    '''
    去掉文件名后缀

    parameter:文件名
    return:去后缀后的文件名
    '''

    mh = filename.rfind('.')
    if mh > 0:
        filename = filename[:mh]
    else:
        filename = filename
    return filename


def to_dir(filename):
    '''
    将类字典冒号分割文本转化为字典对象

    parameter:类字典冒号分割文件名
    return:字典对象
    '''

    data = {}
    file_from = open(filename)
    for line_from in file_from:
        if line:
            if line_from[0] == ':':
                continue
            recs = line_from.split(':')
            rec[0] = rec[0].strip()
            rec[1] = rec[1].strip()
            data[rec[0]] = rec[1]
    return data


def to_data(filename):
    '''
    将类字典冒号分割文本转化为请求头对象

    parameter:类字典冒号分割文件名
    return:请求头对象
    '''

    data = {}
    file_from = open(filename)
    for line_from in file_from:
        if line_from[0] == ':':
            continue
        rec = line_from.split(':')
        rec[0] = rec[0].strip()
        rec[1] = rec[1].strip()
        data[rec[0]] = rec[1]
    import urllib.parse
    data = bytes(urllib.parse.urlencode(data), encoding='utf-8')
    return data


def to_file(filename, to_obj=to_data):
    '''
    将类字典冒号分割文本格式化为同名的,以.pkl为后缀的对象文件

    parameter:类字典冒号分割文件名(str),
              对象转化函数,默认为字典转化函数(function)
    '''

    obj = to_obj(filename)
    filename = process_filename(filename)
    data_file = open(filename + '.pkl', 'wb')
    pickle.dump(obj, data_file)
    data_file.close()


def load_obj(filename):
    '''
    将对象从对象文件中取出

    parameter:文件名
    return:对象
    '''
    data_file = open(filename + '.pkl', 'rb')
    data = pickle.load(data_file)
    data_file.close()
    return data


if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    data1 = to_dir(filename)
    print('data1:', data1)
    to_file(filename)
    data2 = load_obj(filename)
    print('data2:', data2)
