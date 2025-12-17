from panda3d.core import loadPrcFile, Loader
loadPrcFile("Configs\config.prc")

from direct.showbase.ShowBase import ShowBase
from panda3d.core import PointLight, Material
from math import sin, cos

class GameWindow(ShowBase):
    def __init__(self):
        super().__init__()
        self.loader : Loader # Explicit type definition for loader

        self.set_background_color(0, 0, 0, 1)
        self.bombul = self.loader.loadModel('models/Fantastic Turing-Bombul.glb')
        self.bombul.setPos(0, 0, -1)
        self.bombul.setScale(0.5, 0.5, 0.5)
        self.bombul.reparentTo(self.render)

        self.light_model = self.loader.loadModel('models/misc/sphere')
        self.light_model.setScale(0.2, 0.2, 0.2)
        self.light_model.reparentTo(self.render)
        self.light_model.setLightOff()

        self.cam.setPos(0, -12, 0)

        self.lightX = 0
        self.lightSpeed = 2

        pLight = PointLight("pLight")
        
        self.pLightNodePath = self.render.attach_new_node(pLight)
        pLight.setAttenuation((1, 0, 0))
        self.render.setLight(self.pLightNodePath)

        self.taskMgr.add(self.move_light, "move-light")

        print(self.render)
        print(self.camera)
        print(self.cam)
        
    def move_light(self, task):
        dt = globalClock.getDt()

        self.pLightNodePath.setPos(cos(self.lightX)*4, sin(self.lightX)*4, 0)
        self.light_model.setPos(self.pLightNodePath.getPos())
        self.lightX += self.lightSpeed * dt

        return task.cont
    
game = GameWindow()
game.run()
