import requests
from pyquery import PyQuery as pq
from pymongo import MongoClient

headers = {
    'Referer': 'https://m.weibo.cn/u/2830678474',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/67.0.3396.99 Chrome/67.0.3396.99 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    }

baseurl = 'https://m.weibo.cn/api/container/getIndex?'

def get_page(page):

    params = {'type': 'uid',
            'value': '2830678474',
            'containerid': '1076032830678474',
            'page': page
            }
    try:
        response = requests.get(baseurl,headers=headers,params=params)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)


def parse_page(json):
    if json:
        items = json.get('data').get('cards')
        for item in items:
            item = item.get('mblog')
            if not item:
                continue
            weibo = {}
            weibo['id'] = item.get('id')
            weibo['text'] = pq(item.get('text')).text()
            weibo['attitudes'] = item.get('attitudes_count')
            weibo['comments'] = item.get('comments_count')
            weibo['reposts'] = item.get('reposts_count')
            yield weibo


def save_to_mongo(result):
    if collection.insert(result):
        print('Saved to Mongo')


if __name__ == '__main__':
    for page in range(1, 3):
        json = get_page(page)
        results = parse_page(json)
        client = MongoClient('mongodb://admin:admin123@localhost:27017/')
        db = client['weibo']
        collection = db['weibo']
        for result in results:
            save_to_mongo(result)

