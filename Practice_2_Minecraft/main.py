from math import sin, cos, radians as degToRad
from direct.showbase.ShowBase import ShowBase
from panda3d.core import DirectionalLight, AmbientLight
from panda3d.core import TransparencyAttrib
from panda3d.core import WindowProperties, load_prc_file
from panda3d.core import CollisionTraverser, CollisionNode, CollisionBox, CollisionRay, CollisionHandlerQueue
from direct.gui.OnscreenImage import OnscreenImage

load_prc_file('configs/config.prc')

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.selectedBlockType = 'grass'

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

        playerMoveSpeed = 10

        x_movement = 0
        y_movement = 0
        z_movement = 0

        if self.keyMap['forward']:
            x_movement -= dt * playerMoveSpeed * sin(degToRad(camera.getH()))
            y_movement += dt * playerMoveSpeed * cos(degToRad(camera.getH()))
        if self.keyMap['backward']:
            x_movement += dt * playerMoveSpeed * sin(degToRad(camera.getH()))
            y_movement -= dt * playerMoveSpeed * cos(degToRad(camera.getH()))
        if self.keyMap['left']:
            x_movement -= dt * playerMoveSpeed * cos(degToRad(camera.getH()))
            y_movement -= dt * playerMoveSpeed * sin(degToRad(camera.getH()))
        if self.keyMap['right']:
            x_movement += dt * playerMoveSpeed * cos(degToRad(camera.getH()))
            y_movement += dt * playerMoveSpeed * sin(degToRad(camera.getH()))
        if self.keyMap['up']:
            z_movement += dt * playerMoveSpeed
        if self.keyMap['down']:
            z_movement -= dt * playerMoveSpeed

        self.camera.setPos(
            camera.getX() + x_movement,
            camera.getY() + y_movement,
            camera.getZ() + z_movement,
        )

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
        self.keyMap = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False
        }

        self.accept('escape', self.releaseMouse)
        self.accept('mouse1', self.handleLeftClick)
        self.accept('mouse3', self.placeBlock)

        self.accept('w', self.updateKeyMap, ['forward', True])
        self.accept('w-up', self.updateKeyMap, ['forward', False])

        self.accept('s-up', self.updateKeyMap, ['backward', False])
        self.accept('s', self.updateKeyMap, ['backward', True])

        self.accept('a', self.updateKeyMap, ['left', True])
        self.accept('a-up', self.updateKeyMap, ['left', False])

        self.accept('d', self.updateKeyMap, ['right', True])
        self.accept('d-up', self.updateKeyMap, ['right', False])

        self.accept('space', self.updateKeyMap, ['up', True])
        self.accept('space-up', self.updateKeyMap, ['up', False])

        self.accept('lshift', self.updateKeyMap, ['down', True])
        self.accept('lshift-up', self.updateKeyMap, ['down', False])

        self.accept('1', self.setSelectedBlockType, ['grass'])
        self.accept('2', self.setSelectedBlockType, ['dirt'])
        self.accept('3', self.setSelectedBlockType, ['sand'])
        self.accept('4', self.setSelectedBlockType, ['stone'])
        

    def setSelectedBlockType(self, type):
        self.selectedBlockType = type

    def handleLeftClick(self):
        self.captureMouse()
        self.removeBlock()

    def removeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)

            hitNodePath = rayHit.getIntoNodePath()
            hitObject = hitNodePath.getPythonTag('owner')

            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 12:
                hitNodePath.clearPythonTag('owner')
                hitObject.removeNode()
    
    def placeBlock(self):
       if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)
            hitNodePath = rayHit.getIntoNodePath()
            normal = rayHit.getSurfaceNormal(hitNodePath)

            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)



            if distanceFromPlayer < 12:
                hitBoxPos = hitObject.getPos()
                newBlockPos = hitBoxPos + normal * 2
                self.createNewBlock(newBlockPos.getX(), newBlockPos.getY(), newBlockPos.getZ(), self.selectedBlockType)

    def updateKeyMap(self, key, value):
        self.keyMap[key] = value

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

        self.camLens.setFov(90)

        crosshair = OnscreenImage(
            image='assets/png/crosshairs.png',
            pos=(0, 0, 0),
            scale=0.04
        )
        crosshair.setTransparency(TransparencyAttrib.MAlpha)

        self.cTrav = CollisionTraverser()
        ray = CollisionRay()
        ray.setFromLens(self.camNode, (0, 0))
        rayNode = CollisionNode('LOS')
        rayNode.addSolid(ray)
        rayNodePath = self.camera.attachNewNode(rayNode)
        self.rayQueue = CollisionHandlerQueue()
        self.cTrav.addCollider(rayNodePath, self.rayQueue)

    def loadModels(self):
        self.grassBlock = loader.loadModel('assets/glb/grass-block.glb')
        self.dirtBlock = loader.loadModel('assets/glb/dirt-block.glb')
        self.stoneBlock = loader.loadModel('assets/glb/stone-block.glb')
        self.sandBlock = loader.loadModel('assets/glb/sand-block.glb')

    def generateTerrain(self):
        for z in range(10):
            for y in range(20):
                for x in range(20):
                    self.createNewBlock(
                        x * 2 - 20,
                        y * 2 - 20,
                        -z * 2,
                        'grass' if z == 0 else 'dirt'
                    )

    def createNewBlock(self, x, y, z, type):
        newBlockNode = render.attachNewNode('new block placeholder')
        newBlockNode.setPos(x, y, z)

        if type == 'grass':
            self.grassBlock.instanceTo(newBlockNode)
        elif type == 'dirt':
            self.dirtBlock.instanceTo(newBlockNode)
        elif type == 'sand':
            self.sandBlock.instanceTo(newBlockNode)
        elif type == 'stone':
            self.stoneBlock.instanceTo(newBlockNode)

        blockSolid = CollisionBox((-1, -1, -1), (1, 1, 1))
        blockNode = CollisionNode('block-collision-node')
        blockNode.addSolid(blockSolid)
        collider = newBlockNode.attachNewNode(blockNode)
        collider.setPythonTag('owner', newBlockNode)

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
