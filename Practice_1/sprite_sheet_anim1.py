from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData, CardMaker, TransparencyAttrib, TextureStage

configVars = """
win-size 1920 1080
show-frame-rate-meter True 
window-title Sprite Sheet Animation Example
"""

loadPrcFileData("", configVars)

class GameWindow(ShowBase):
    def __init__(self):
        super().__init__()

        self.set_background_color(0.1, 0.1, 0.1, 1)

        cm = CardMaker("sprite")
        cm.setFrame(-1, 1, -1, 1) # Creates a plane
        cm.setUvRange((0.0, 0.0), (0.5, 1.0)) # First frame only cropping
        
        self.plane = render.attachNewNode(cm.generate())

        texture = loader.loadTexture("models/knight.png")
        
        # Texture Filtering
        texture.setMinfilter(texture.FTNearest)
        texture.setMagfilter(texture.FTNearest)

        self.plane.setTexture(texture)
        self.plane.setTransparency(TransparencyAttrib.MAlpha)

        self.tx = 0.0
        self.tx_offset = 1 / 2
        self.texture_update = 0

        self.taskMgr.add(self.update_texture, "Update texture")

    def update_texture(self, task):
        self.plane.setTexOffset(TextureStage.getDefault(), self.tx, 0)

        self.texture_update += 1
        if self.texture_update > 100: # Update animation every X frames
            self.tx += self.tx_offset
            self.texture_update = 0

        return task.cont
        
        
game = GameWindow()
game.run()
