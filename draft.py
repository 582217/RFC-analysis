import requests
import os
from lxml import etree
import json


def get_names_set(file_dir):
    l_fname = set()
    for root, dirs, files in os.walk(file_dir):
        for name in files:
            l_fname.add(name.rsplit('-', 1)[0])
    return l_fname


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


def get_page(url):
    retry_count = 5
    proxy = get_proxy().get("proxy")
    while retry_count > 0:
        try:
            html = requests.get(url, proxies={
                                "http": "http://{}".format(proxy)})
            # 使用代理访问
            return html
        except Exception:
            retry_count -= 1
    delete_proxy(proxy)
    return None


s_names = get_names_set(r"D:\id")
l_failnames = []
d_res = {}

while len(s_names):
    print(len(s_names))
    name = s_names.pop()
    try:
        search_url = 'https://datatracker.ietf.org/doc/search?name='+name + \
            '&sort=&rfcs=on&activedrafts=on&olddrafts=on&by=group&group='
        page = get_page(search_url)
        tree = etree.HTML(page.text)
        serch_res = tree.xpath(
            '//*[@id="content"]/table/tbody[1]/tr/th[2]')[0].text
        att = tree.xpath(
            '//*[@id="content"]/table/tbody[2]/tr/td[2]/div/a')[0].attrib
        doc_name = att['href'].split('/')[2]

        print('serch res  '+serch_res)

        json_url = 'https://datatracker.ietf.org'+att['href']+'doc.json'
        jpage = get_page(json_url).text
        data = json.loads(jpage)
        h_count = len(data['rev_history'])
        d_res[name] = [doc_name, serch_res.strip(), h_count]
    except:
        l_failnames.append(name)
        print('fail  '+name)
