'''
爬取淘宝商品信息,通过selenium获得渲染后的源码,pyquery解析,mongodb存储
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery as pq
import pymongo

BASEURL = 'https://s.taobao.com/search?q='
KEYWORD = 'python'
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
client = pymongo.MongoClient('mongodb://admin:admin123@localhost:27017/')
db = client.taobao
collection = db.products

def get_page(page):
    ```
    跳转到传入页面,获得源码,调用商品解析函数
    ```

    #driver = webdriver.Chrome()
    #wait = WebDriverWait(driver, 10)
    try:
        driver.get(BASEURL + quote(KEYWORD))
        print('你当前访问的是第%d页' % page)
        if page > 1:
            J_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input' )))
            J_submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
            J_input.clear()
            J_input.send_keys(page)
            J_submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,
            '#mainsrp-pager li.item.active > span'), str(page)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
        html = driver.page_source
        get_products(html)
    except TimeoutException:
        print('try again')
        get_page(page)


def get_products(html):
    '''
    解析出每件商品信息,调用存储函数存储
    '''

    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {}
        product['image'] = item.find('.img').attr('src')
        product['price'] = item.find('.price').text()
        product['payment'] = item.find('.deal-cnt').text()
        product['title'] = item.find('.title').text()
        product['location'] = item.find('.location').text()
        product['shop'] = item.find('.shopname').text()
        product['shop-link'] = item.find('.shopname').attr('href')
        print(product)
        save_to_mongo(product)


def save_to_mongo(product):
    ```
    存储函数,将商品信息存入数据库
    ```

    try:
        if collection.insert(product):
            print('存储成功')
    except Exception as e:
            print('失败',e.__class__)


if __name__ == '__main__':
    for i in range(1, 3):
        get_page(i)

