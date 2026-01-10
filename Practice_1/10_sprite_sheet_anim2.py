from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData

configVars = """
win-size 1920 1080
show-frame-rate-meter True 
window-title Sprite Sheet Animation Example 2
"""

loadPrcFileData("", configVars)

class GameWindow(ShowBase):
    def __init__(self):
        super().__init__()
        self.set_background_color(0.1, 0.1, 0.1, 1)
        self.cam.setPos(0, -5, 0)

        self.knight = self.loader.loadModel("assets/texture_cards/Knight")
        self.knight.reparentTo(self.render)
    
        
game = GameWindow()
game.run()
