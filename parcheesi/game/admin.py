from django.contrib import admin
#from .models import Game
#from .models import Player
#from .models import Cell
#from .models import Artifact
#from .models import Action
#from .models import GameLog
#from .models import ActionName
#from .models import Card
from .models import *
admin.site.register(Game)
admin.site.register(Player)
admin.site.register(Cell)
admin.site.register(Artifact)
admin.site.register(Action)
admin.site.register(ActionName)
admin.site.register(GameLog)
admin.site.register(Card)