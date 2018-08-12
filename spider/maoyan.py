'''
抓取猫眼国内票房榜,地址:http://maoyan.com/board/1
'''

import re
import requests


def  one_page(url):
    '''
    获取页面
    '''
    
    headers = {
            'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/67.0.3396.99 Chrome/67.0.3396.99 Safari/537.36',
            'referer': 'http://maoyan.com/board/4'
            }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except requests.RequestsException as e:
        print(e.reason)
        return None


def parse_page(html):
    '''
    解析页面
    '''
    
    patter = re.compile('class="board-index\sboard-index-\d+">(\d{0,3})</i>.*?data-src="(.*?)".*?class="name"><a.*?>(.*?)</a></p>.*?class="star">(.*?)</p>.*?class="releasetime">(.*?)</p>', re.S)
    print("1")
    rec_list = re.findall(patter, html)
    print("2")
    for rec in rec_list:
        print('排名 = %s, 图片链接 = %s, 名字 = %s, 主演 = %s, 时间 = %s' % (rec[0], rec[1], rec[2], rec[3], rec[4]))


if __name__ == '__main__':
    html = open('html.txt').read()
    parse_page(html)

