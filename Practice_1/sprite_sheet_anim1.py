from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData, CardMaker, TransparencyAttrib

configVars = """
win-size 1920 1080
show-frame-rate-meter True
"""

loadPrcFileData("", configVars)

class GameWindow(ShowBase):
    def __init__(self):
        super().__init__()

        self.set_background_color(0.1, 0.1, 0.1, 1)

        cm = CardMaker("sprite")
        cm.setFrame(-1, 1, -1, 1)  # Creates a plane from (-1, -1) to (1, 1)
        
        plane = render.attachNewNode(cm.generate())

        texture = loader.loadTexture("models/knight.png")
        
        # Texture Filtering
        texture.setMinfilter(texture.FTNearest)
        texture.setMagfilter(texture.FTNearest)

        plane.setTexture(texture)
        plane.setTransparency(TransparencyAttrib.MAlpha)

        self.taskMgr.add(self.updateManagers, "Update texture")

    def update_texture(self, task):

        return task.cont
        
        
game = GameWindow()
game.run()
