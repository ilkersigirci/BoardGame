from django.conf.urls import url

from . import views

urlpatterns = [
    url('about/', views.about, name='game-about'),
    url('', views.home, name='game-home'),
]
