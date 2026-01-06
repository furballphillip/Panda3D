from panda3d.core import loadPrcFile, Loader
loadPrcFile("Configs\config.prc")

from direct.showbase.ShowBase import ShowBase
from panda3d.core import PointLight, AmbientLight, NodePath
from math import sin, cos
from direct.filter.CommonFilters import CommonFilters

class LightsAndShadows(ShowBase):
    def __init__(self):
        super().__init__()
        self.loader : Loader # Explicit type definition for loader

        self.set_background_color(0, 0, 0, 1)
        self.cam.setPos(0, -12, 0)

        self.bombul = NodePath("bombul")
    
        self.bombul1 = self.loader.loadModel('models/Fantastic Turing-Bombul.glb')
        self.bombul1.setPos(0, 0, -3)
        self.bombul.setScale(0.5, 0.5, 0.5)
        self.bombul1.reparentTo(self.bombul)

        self.bombul2 = self.loader.loadModel('models/Fantastic Turing-Bombul.glb')
        self.bombul2.setPos(4, 7, -3)
        self.bombul.setScale(0.5, 0.5, 0.5)
        self.bombul2.reparentTo(self.bombul)

        self.bombul3 = self.loader.loadModel('models/Fantastic Turing-Bombul.glb')
        self.bombul3.setPos(-4, 7, -3)
        self.bombul.setScale(0.5, 0.5, 0.5)
        self.bombul3.reparentTo(self.bombul)

        self.bombul.reparentTo(self.render)

        self.floor = self.loader.loadModel('models/floor')
        self.floor.setPos(0, 0, -2.5)
        self.floor.reparentTo(self.render)

        self.light_model = self.loader.loadModel('models/misc/sphere')
        self.light_model.setScale(0.2, 0.2, 0.2)
        self.light_model.reparentTo(self.render)
        self.light_model.setLightOff()

        pLight = PointLight("pLight")
        pLight.setShadowCaster(True, 1024, 1024)
        self.render.setShaderAuto()
        pLightNodePath = self.light_model.attachNewNode(pLight)
        self.bombul.setLight(pLightNodePath)

        aLight = AmbientLight("aLight")
        aLight.setColor((0.04, 0.04, 0.04, 1))
        aLightNodePath = self.render.attachNewNode(aLight)
        self.bombul.setLight(aLightNodePath)

        self.floor.setLight(pLightNodePath)
        self.floor.setLight(aLightNodePath)

        filters = CommonFilters(self.win, self.cam)
        filters.setBloom(size="large")

        self.taskMgr.add(self.move_light, "move-light")

    def move_light(self, task):
        ft = globalClock.getFrameTime()

        self.light_model.setPos(cos(ft)*3, sin(ft)*3, 0)

        return task.cont

       
    
game = LightsAndShadows()
game.run()
