from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('about/', views.about, name='game-about'),
    path('', views.home, name='game-home'),
    path('<int:game_id>/details/', views.detail, name='game-detail'),
    path('<int:game_id>/next/', views.game_next, name='game-next'),
    path('<int:game_id>/pick/', views.pick, name='game-pick'),
    path('<int:game_id>/join/', views.join, name='game-join'),
    path('<int:game_id>/ready/', views.ready, name='game-ready'),
]
