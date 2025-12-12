from panda3d.core import loadPrcFile, Loader, NodePath
loadPrcFile("Configs/config.prc")

from direct.showbase.ShowBase import ShowBase
from math import sin, cos

character_model_path = "Character.glb" 

class GameWindow(ShowBase):
    def __init__(self):
        super().__init__()

        self.loader: Loader # Explicit type definition

        self.cam.setPos(0, -10, 0)

        self.jack = self.loader.loadModel("models/jack")
        self.jack.setHpr(0, 180, 180)
        self.jack.reparentTo(self.render)

        self.panda = self.loader.loadModel("models/panda")
        self.panda.setScale(0.2, 0.2, 0.2)
        self.panda.setPos(2, 0, 0)
        self.panda.reparentTo(self.render)
        
        self.teapot = self.loader.loadModel("models/teapot")
        self.teapot.setScale(0.2)
        self.teapot.setPos(-2, 0, 0)
        self.teapot.setColor(1, 0, 0, 1)
        self.teapot.reparentTo(self.render)

        self.sphere = self.loader.loadModel("models/misc/sphere")
        self.sphere.setScale(0.2)
        self.sphere.setColor(0, 1, 0, 1)
        self.sphere.reparentTo(self.render)
        
        self.x = 0
        self.speed = 2
        self.angle = 0
        self.taskMgr.add(self.updateTask, "update")

    def updateTask(self, task):
        dt = globalClock.getDt() # type: ignore
        print(f"Delta Time: {dt}")

        self.panda.setH(self.angle)
        self.teapot.setHpr(self.angle, 0, self.angle)
        self.sphere.setPos(cos(self.x)*4, sin(self.x)*4, cos(self.x)*2)
        self.jack.lookAt(self.sphere)


        self.angle += 1
        self.x += self.speed * dt
    
        return task.cont
    
game = GameWindow()
game.run()
