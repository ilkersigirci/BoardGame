def notify_user(self,descr=""):
        sizeof = len(self.players)
		for i in range(0,sizeof):
            (self.players[i]).turn("roll")
            yield True
            if i == sizeof-1:
                if(self.cycles):
                    i = 0
                # else terminate
            

            

			player.turn("roll")
		for user in self.callbacks:
            self.callbacks[user]("Item state changed")