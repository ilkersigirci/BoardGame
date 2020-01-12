from django.contrib import admin
from .models import *
admin.site.register(Game)
admin.site.register(Player)
admin.site.register(Cell)
admin.site.register(Artifact)
admin.site.register(Action)
admin.site.register(ActionName)
admin.site.register(GameLog)
admin.site.register(Card)