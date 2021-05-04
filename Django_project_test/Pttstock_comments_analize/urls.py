from django.contrib import admin
from django.urls import include, path
from .views import Viewwordcloud, get_name

urlpatterns = [
    path('formtest/', get_name, name='get_name'),
    path('wordcloud/', Viewwordcloud.as_view(), name='get_wordcloud'),
]