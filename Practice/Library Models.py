from panda3d.core import loadPrcFile, Loader
loadPrcFile("Configs/config.prc")

from direct.showbase.ShowBase import ShowBase

class GameWindow(ShowBase):
    loader: Loader
    
    def __init__(self):
        super().__init__()

        env = self.loader.loadModel("models/environment")
        env.reparentTo(self.render)

        box = self.loader.loadModel("models/box")
        box.setPos(0, 10, 0)
        box.reparentTo(self.render)

        panda = self.loader.loadModel("models/panda")
        panda.setPos(1, 15, 0)
        panda.setScale(0.3, 0.3, 0.3)
        panda.reparentTo(self.render)

game = GameWindow()
game.run()
