from django.conf.urls import url
from django.urls import path
from .views import login, userList, userDetail

urlpatterns = [
    path('login/', login.as_view()),
    #path('logout/', logout.as_view()),
    path('userList/', userList.as_view()),
    path('userDetail/', userDetail.as_view()),
]
