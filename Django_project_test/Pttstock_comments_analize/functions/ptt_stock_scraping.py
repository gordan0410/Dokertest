from Pttstock_comments_analize.models import Ptt_stock_comments
from bs4 import BeautifulSoup
import requests
import time


# 找出文章url
def find_article_url(url_index, today, title=False):
    resp = requests.get(url_index)
    soup = BeautifulSoup(resp.text, 'html5lib')
    articles = soup.find_all('div', 'title')
    title_list = []

    if title:
        title_list = title
    else:
        name_list = ['後','中','前']
        for name in name_list:
            title_list.append('[閒聊] ' + today + ' 盤' + name + '閒聊')

    for article in articles:
        article_title = article.text.strip()
        if article_title in title_list:
            return article.a['href']
    return None


def find_comment(article_url):
    comment_list = []
    resp = requests.get(article_url)
    soup = BeautifulSoup(resp.text, 'html5lib')
    comments = soup.select('div.push span.f3.push-content')
    for comment in comments:
        comment_list.append(comment.text.strip()[2:])

    return comment_list


def crawl_ptt_stock(title=False):
    # 今日時間+起始頁面
    today = time.strftime('%Y/%m/%d')
    url_index = "https://www.ptt.cc/bbs/Stock/"
    article = find_article_url(url_index, today, title)
    if article:
        comment_list = find_comment(url_index + article.split("/")[3])
        for c in comment_list:
            obj, created = Ptt_stock_comments.objects.update_or_create(
               comment=c, defaults={'date': today.replace("/", "-")}
            )
    else:
        print("get url failed")
