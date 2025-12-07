# from panda3d.core import loadPrcFile
# loadPrcFile("Configs\config.prc")

from panda3d.core import loadPrcFileData

configVars = """
win-size 1920 1080
window-title Game Window
show-frame-rate-meter True
undecorated False
"""

loadPrcFileData("", configVars)

from direct.showbase.ShowBase import ShowBase

class GameWindow(ShowBase):
    def __init__(self):
        super().__init__()

        print(self.render)
        print(self.camera)
        print(self.cam)
        
game = GameWindow()
game.run()
