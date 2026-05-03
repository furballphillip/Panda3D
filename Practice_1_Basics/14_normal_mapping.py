from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData, PointLight, AmbientLight
import math

configVars = """
win-size 1920 1080
show-frame-rate-meter True 
"""

loadPrcFileData("", configVars)

class GameWindow(ShowBase):
    def __init__(self):
        super().__init__()
        self.loader : Loader # Explicit type definition for loader

        self.set_background_color(0, 0, 0, 1)
        self.cam.setPos(0, -20, 5)

        self.plane = self.loader.loadModel('assets/models/egg/planeTB')
        self.plane.setPos(-5, 5, 0)
        self.plane.reparentTo(self.render)

        self.sphere = self.loader.loadModel("assets/models/egg/icosphere")
        self.sphere.reparentTo(self.render)

        aLight = AmbientLight('alight')
        aLight.setColor((0.2, 0.2, 0.2, 1))
        alnp = self.render.attachNewNode(aLight)
        self.plane.setLight(alnp)

        pLight = PointLight('plight')
        pLight.setColor((1, 1, 1, 1))
        plnp = self.sphere.attachNewNode(pLight)
        self.plane.setLight(plnp)

        self.render.setShaderAuto()

        self.taskMgr.add(self.move_light, "move-light")

    def move_light(self, task):
        ft = globalClock.getFrameTime()

        self.sphere.setPos(math.sin(ft) * 10, 0, 5)

        return task.cont


game = GameWindow()
game.run()
