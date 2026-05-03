from direct.showbase.ShowBase import ShowBase
from panda3d.core import DirectionalLight, AmbientLight
from panda3d.core import TransparencyAttrib
from panda3d.core import WindowProperties
from direct.gui.OnscreenImage import OnscreenImage

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.captured = True

        self.loadModels()
        self.setLights()
        self.generateTerrain()
        self.setCamera()
        self.setSkybox()
        self.captureMouse()
        self.setControls()

        taskMgr.add(self.update, 'update')

    def update(self, task):
        dt = globalClock.getDt()

        if self.captured:
            md = self.win.getPointer(0)
            mouseX = md.getX()
            mouseY = md.getY()

            mouseChangeX = mouseX - self.lastMouseX
            mouseChangeY = mouseY - self.lastMouseY

            self.cameraSwingFactor = 10

            currentH = self.camera.getH()
            currentP = self.camera.getP()

            self.camera.setHpr(
                currentH - mouseChangeX * dt * self.cameraSwingFactor,
                min(90, max(-90, currentP - mouseChangeY * dt * self.cameraSwingFactor)),
                0
            )

            self.win.movePointer(0,
                self.win.getXSize() // 2,
                self.win.getYSize() // 2
            )

            self.lastMouseX = self.win.getXSize() // 2
            self.lastMouseY = self.win.getYSize() // 2

        return task.cont

    def setControls(self):
        self.accept('escape', self.releaseMouse)
        self.accept('mouse1', self.captureMouse)

    def captureMouse(self):
        self.captured = True
        self.cameraSwingActivated = True

        properties = WindowProperties()
        properties.setCursorHidden(True)
        properties.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(properties)

        if base.mouseWatcherNode.hasMouse():
            self.win.movePointer(0,
                self.win.getXSize() // 2,
                self.win.getYSize() // 2
            )
            self.lastMouseX = self.win.getXSize() // 2
            self.lastMouseY = self.win.getYSize() // 2
        else:
            md = self.win.getPointer(0)
            self.lastMouseX = md.getX()
            self.lastMouseY = md.getY()
    
    def releaseMouse(self):
        self.captured = False

        self.cameraSwingActivated = False
        properties = WindowProperties()
        properties.setCursorHidden(False)
        properties.setMouseMode(WindowProperties.M_relative)
        self.win.requestProperties(properties)

    def setCamera(self):
        self.disableMouse()
        self.camera.setPos(0, 0, 3)

        crosshair = OnscreenImage(
            image='assets/png/crosshairs.png',
            pos=(0, 0, 0),
            scale=0.04
        )
        crosshair.setTransparency(TransparencyAttrib.MAlpha)

    def loadModels(self):
        self.grassBlock = loader.loadModel('assets/glb/grass-block.glb')
        self.dirtBlock = loader.loadModel('assets/glb/dirt-block.glb')
        self.stoneBlock = loader.loadModel('assets/glb/stone-block.glb')
        self.sandBlock = loader.loadModel('assets/glb/sand-block.glb')

    def generateTerrain(self):
        for z in range(10):
            for y in range(20):
                for x in range(20):
                    newBlockNode = render.attachNewNode('new block placeholder')

                    newBlockNode.setPos(
                        x * 2 - 20,
                        y * 2 - 20,
                        -z * 2
                    )

                    if z == 0:
                        self.grassBlock.instanceTo(newBlockNode)
                    else:
                        self.dirtBlock.instanceTo(newBlockNode)

    def setLights(self):
        dLight = DirectionalLight('directional Light')
        dLightNodePath = render.attachNewNode(dLight)
        dLightNodePath.setHpr(30, -60, 0)
        render.setLight(dLightNodePath)

        aLight = AmbientLight('ambient Light')
        aLight.setColor((0.2, 0.2, 0.2, 1))
        aLightNodePath = render.attachNewNode(aLight)
        render.setLight(aLightNodePath)

    def setSkybox(self):
        skybox = loader.loadModel('assets/skybox.egg')
        skybox.setScale(100)
        skybox.setBin('background', 1)
        skybox.setDepthWrite(0)
        skybox.setLightOff()
        skybox.reparentTo(render)

game = Game()
game.run()
