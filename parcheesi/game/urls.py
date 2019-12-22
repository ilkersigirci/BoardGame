from django.conf.urls import url
from django.urls import path


from . import views

urlpatterns = [
    path('about/', views.about, name='game-about'),
    path('', views.home, name='game-home'),
    path('<int:game_id>/', views.detail, name='game-detail'),
]
