import os
from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from .models import Ptt_stock_comments
from .forms import NameForm, DateForm
import datetime
import matplotlib.image as mpimg
from django.conf import settings
import jieba
import json
# Create your views here.


# with index.html
def index_page(request):
    return render(request, "index.html")


# with name.html
def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = form['your_name']
            email = form['your_email']
            return HttpResponseRedirect('/admin/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'name.html', {'form': form})


class Viewwordcloud(View):
    # with word_cloud.html
    template_name = "word_cloud.html"
    form_class = DateForm
    today = datetime.date.today()


    def calculate_date(self):
        holiday_list = []
        date_list = []
        with open(settings.BASE_DIR + '/Pttstock_comments_analize/functions/TWholiday.json', encoding='utf-8-sig', errors='ignore') as f:
            data = json.loads(f.read())
            for index in range(len(data)):
                holiday_list.append(data[index]['date'])

        for c in range(7):
            date = self.today - datetime.timedelta(days=c)
            date_list.append(date)
        return date_list, holiday_list

    def calculate_term_frequency(self):
        date_list, holiday_list = self.calculate_date()
        weekly_dict_list = []
        for date in date_list:
            daily_string = ''
            count = 0
            daily_dict = {}
            result = {}
            daily_terms = Ptt_stock_comments.objects.filter(date=date.strftime('%Y-%m-%d'))
            for daily_term in daily_terms:
                daily_string += daily_term.comment
            # remove stop words begin
            with open(settings.BASE_DIR + '/Pttstock_comments_analize/functions/stop_word.txt', 'r') as f:
                stop_words = f.readlines()
            stop_words = [stop_word.rstrip() for stop_word in stop_words]
            str_list = []
            daily_list = list(jieba.cut(daily_string))
            for seg in daily_list:
                if seg not in stop_words:
                    str_list.append(seg)
            for word in str_list:
                if word in daily_dict:
                    daily_dict[word] += 1
                else:
                    daily_dict[word] = 1
            daily_dict = dict(sorted(daily_dict.items(), key=lambda item: item[1], reverse=True))
            for k,v in daily_dict.items():
                if count <= 6:
                    if not k == ' ':
                        result[k] = v
                else:
                    break
                count += 1
            print(result)
            weekly_dict_list.append(result)
        return weekly_dict_list

    def get(self, request):
        weekly_dict_list = self.calculate_term_frequency()
        date_form = self.form_class
        d_list, h_list = self.calculate_date()
        d_list = [d.strftime('%Y-%m-%d') for d in d_list]
        return render(request, self.template_name, locals())

    def post(self, request):
        file_exist = False
        weekly_dict_list = self.calculate_term_frequency()
        date_form = self.form_class(request.POST)
        d_list, h_list = self.calculate_date()
        d_list = [d.strftime('%Y-%m-%d') for d in d_list]
        if date_form.is_valid():
            date = date_form['search_date']
            if os.path.exists(settings.BASE_DIR + '/media/Pttstock_comments_analize/' + date.value() + ".png"):
                file_exist = True
        return render(request, self.template_name, locals())


