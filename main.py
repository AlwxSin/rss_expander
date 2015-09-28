__author__ = 'Alwx'

import requests
from lxml import html, etree


r = requests.get('http://mmozg.net/rss/index/')

parser = etree.XMLParser(encoding=r.encoding)
root = etree.fromstring(r.content.lstrip(), parser=parser)

xpath = '//*[@id="content"]/article[1]'

def article(link, xpath):
    r = requests.get(link)
    content = r.content.lstrip()
    parser = etree.HTMLParser(encoding=r.encoding)
    tree = html.fromstring(content, None, parser)
    elem = tree.xpath(xpath)[0]
    final = etree.tostring(elem, pretty_print=True, encoding=r.encoding)
    return final

items = root.find('channel').findall('item')
for item in items:
    link = item.find('link').text
    full_article = article(link, xpath)
    if full_article:
        item.find('description').text = unicode(full_article, 'utf-8')

full_rss = etree.tostring(root, encoding=r.encoding)
