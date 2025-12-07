from panda3d.core import loadPrcFile, Loader
loadPrcFile("Configs/config.prc")

from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath

class GameWindow(ShowBase):
    loader: Loader # Explicit type definition for loader
    
    def __init__(self):
        super().__init__()

        empty = NodePath("empty")

        env = self.loader.loadModel("models/environment")
        env.reparentTo(self.render)

        box = self.loader.loadModel("models/box")
        box.setPos(0, 5, 0)
        box.reparentTo(empty)
        boxNode = box.node()
        print(type(box))
        print(type(boxNode))

        panda = self.loader.loadModel("models/panda")
        panda.setPos(2, 0, 0)
        panda.setScale(0.3, 0.3, 0.3)
        panda.reparentTo(box)

        empty.reparentTo(self.render)

game = GameWindow()
game.run()
