from direct.showbase.ShowBase import ShowBase

class GameWindow(ShowBase):
    def __init__(self):
        super().__init__()

        print(self.render)
        print(self.camera)
        print(self.cam)
        
game = GameWindow()
game.run()
