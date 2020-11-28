from django.conf.urls import url
from django.urls import path
from .views import taskList, taskDetail

urlpatterns = [
    path('taskList/', taskList.as_view()),
    path('taskDetail/', taskDetail.as_view()),
]
