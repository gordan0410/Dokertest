import jieba
from django.conf import settings
from wordcloud import WordCloud
from time import strftime
from Pttstock_comments_analize.models import Ptt_stock_comments


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
    print(return_list)
    return return_list


def word_cloud(data_list=False, date=strftime('%Y-%m-%d')):
    if data_list:
        comment_list = data_list
    else:
        dl = Ptt_stock_comments.objects.filter(date=date).values_list('comment', flat=True)
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
    cloud.to_file(settings.MEDIA_ROOT + 'Pttstock_comments_analize/' + date + '.png')





