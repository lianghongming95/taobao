__author__ = 'Administrator'
from selenium import webdriver
from urllib.parse import quote
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import pymongo



browser = webdriver.Chrome()

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
# browser = webdriver.Chrome(chrome_options=chrome_options)
url = "https://s.taobao.com/search?q=" + quote("ipad")
print(url)


def index_page(page):
    browser.get(url)

    if page>1:
        input = WebDriverWait(browser,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#mainsrp-pager > div > div > div > div.form > input")))
        submit =WebDriverWait(browser,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit")))
        input.clear()
        input.send_keys(page)
        submit.click()

    WebDriverWait(browser,20).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,"#mainsrp-pager > div > div > div > ul > li.item.active > span"),str(page)))
    WebDriverWait(browser,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,".m-itemlist .items .item")))
    html = browser.page_source
    # print(html)
    doc = pq(html)
    # print(doc)
    items = doc("#mainsrp-itemlist .items .item").items()
    print(items)
    for item in items:
        product = {
            "image":item.find(".pic .img").attr("data-src"),
            "price":item.find(".price").text(),
            "deal":item.find(".deal-cnt").text(),
            "title":item.find(".title").text(),
            "shop":item.find(".shop").text(),
            "location":item.find(".location").text()

        }
        print(product)
        save_to_mongodb(product)

MONGO_URL = "localhost"
MONGO_DB = "taobaoipad20180923"
MONGO_COLLECTION = "products"
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

def save_to_mongodb(result):

    if db[MONGO_COLLECTION].insert(result):
        print("存储成功")


def main():
    for i in range(1,101):
        index_page(i)


# index_page(2)