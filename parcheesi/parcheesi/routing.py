from django.conf.urls import url
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from game.consumers import GameConsumer, TaskConsumer
application = ProtocolTypeRouter({
    # Empty for now
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    #url(r"", GameConsumer, name='game-consumer')
                    path('<int:game_id>/details/', GameConsumer, name='game-detail-consumer'),
                    #path('about/', views.about, name='game-about'),
                    #path('', views.home, name='game-home'),
                    #path('<int:game_id>/next/', views.game_next, name='game-next'),
                    #path('<int:game_id>/pick/', views.pick, name='game-pick'),
                    #path('<int:game_id>/join/', views.join, name='game-join'),
                    #path('<int:game_id>/ready/', views.ready, name='game-ready'),
                ]
            )
        ),
    ),
    # burasi degismesi lazim
    'channel': ChannelNameRouter({
        'task': TaskConsumer
    })
})