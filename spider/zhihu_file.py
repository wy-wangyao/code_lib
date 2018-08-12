# 爬取知乎发现页面,用文件存储

import requests
from pyquery import PyQuery as pq


def get_html(url):
    '''根据网址获取html页面
    
    parameter:url目标网址
    return:html页面
    '''
    
    headers = {
            'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/67.0.3396.99 Chrome/67.0.3396.99 Safari/537.36'
            }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            html = response.text
            print('OK')
            return html
        else:
            return print('request failure>')
    except requests.RequestException:
        return print('error')


def get_file(filename, html):
    '''从html页面解析出文本,写入文件
    
    parameter:文件名,html页面
    '''
    doc = pq(html)
    items = doc('.explore-tab .feed-item').items()
    for item in items:
        question = item.find('.question_link').text()
        author = item.find('.author-link').text()
        answer = pq(item.find('.content').html()).text()
        file = open(filename, 'a', encoding='utf-8')
        file.write('\n'.join([question, author, answer]))
        file.write('\n' + '='*50 + '\n')
        file.close()


if __name__ == '__main__':
    html = get_html('https://www.zhihu.com/explore')
    get_file('zhihu.txt', html)
