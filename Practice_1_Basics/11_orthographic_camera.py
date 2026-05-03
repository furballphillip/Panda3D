from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData, OrthographicLens

configVars = """
win-size 1920 1080
show-frame-rate-meter True 
window-title Sprite Sheet Animation Example 2
"""

loadPrcFileData("", configVars)

class GameWindow(ShowBase):
    def __init__(self):
        super().__init__()
        self.loader : Loader # Explicit type definition for loader

        self.set_background_color(0.1, 0.1, 0.1, 1)
        self.cam.setPos(0, -5, 0)

        self.cube1 = self.loader.loadModel("models/box")
        self.cube1.setPos(1, 0, 0)
        self.cube1.setScale(50)
        self.cube1.reparentTo(self.render)

        self.cube2 = self.loader.loadModel("models/box")
        self.cube2.setPos(-70, 8, 0)
        self.cube2.setScale(50)
        self.cube2.reparentTo(self.render)

        lens = OrthographicLens()
        lens.setFilmSize(1980, 1080)
        lens.setNearFar(-50, 50)
        self.cam.node().setLens(lens)
    
        
game = GameWindow()
game.run()
