from Pttstock_comments_analize.models import Ptt_stock_comments
from bs4 import BeautifulSoup
import requests
import jieba
from django.conf import settings
from wordcloud import WordCloud
from time import strftime
from datetime import date


def find_article_url(url_index, today, title=False):
    # 找出文章url
    finish = True
    resp = requests.get(url_index)

    while finish:
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
                finish = False
                return article.a['href']
        next_page = soup.find('div', 'btn-group btn-group-paging').find_all('a')[1]['href']
        resp = requests.get("https://www.ptt.cc" + next_page)


def find_comment(article_url):
    comment_list = []
    resp = requests.get(article_url)
    soup = BeautifulSoup(resp.text, 'html5lib')
    comments = soup.select('div.push span.f3.push-content')
    for comment in comments:
        comment_list.append(comment.text.strip()[2:])

    return comment_list


def crawl_ptt_stock(title=False, today=date.today().strftime('%Y/%m/%d')):
    # 今日時間+起始頁面

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


def remove_stop_words(stop_word_file, seg_list):
    with open(stop_word_file, 'r') as f:
        stop_words = f.readlines()
    stop_words = [stop_word.rstrip() for stop_word in stop_words]
    str_list = ''
    for seg in seg_list:
        if seg not in stop_words:
            str_list += seg + " "
    return str_list


def word_proc_jieba(data_list):
    return_list = []
    for e in data_list:
        return_list += jieba.lcut(e)
    return return_list


def word_cloud(data_list=False, date=date.today().strftime('%Y/%m/%d')):
    date_pro = date.replace("/", "-")

    if data_list:
        comment_list = data_list
    else:
        dl = Ptt_stock_comments.objects.filter(date=date_pro).values_list('comment', flat=True)
        comment_list = []
        for d in dl:
            comment_list.append(d)

    proc = word_proc_jieba(comment_list)
    font = settings.BASE_DIR + '/Pttstock_comments_analize/functions/msjhl.ttc'
    after_proc = remove_stop_words(settings.BASE_DIR + '/Pttstock_comments_analize/functions/stop_word.txt', proc)
    wc = WordCloud(
        font_path=font,
        height=600,
        width=800,
    )
    cloud = wc.generate(after_proc)
    cloud.to_file(settings.MEDIA_ROOT + 'Pttstock_comments_analize/' + date_pro + '.png')


def show_word_cloud(title=False, date=date.today().strftime('%Y/%m/%d'), datalist=False):
    crawl_ptt_stock(title, date)
    word_cloud(datalist, date)

