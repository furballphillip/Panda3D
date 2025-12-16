from panda3d.core import loadPrcFile, Loader, NodePath
loadPrcFile("Configs/config.prc")

from direct.showbase.ShowBase import ShowBase

keyMap = {
    "up": False,
    "down": False,
    "left": False,
    "right": False,
    "rotate": False,
}

def updateKeyMap(key, state):
    keyMap[key] = state

class GameWindow(ShowBase):
    def __init__(self):
        super().__init__()
        self.loader: Loader

        self.cam.setPos(0, -10, 0)

        self.jack = self.loader.loadModel("models/jack") # type: ignore
        self.jack.setHpr(0, 180, 180)
        self.jack.reparentTo(self.render)

        # disable default mouse controls
        self.disable_mouse()

        # Mouse binds
        self.accept("mouse1", self.mouse_click)
        self.accept("mouse1-up", self.mouse_click)
        self.accept("mouse2", self.mouse_click)
        self.accept("mouse2-up", self.mouse_click)
        self.accept("mouse3", self.mouse_click)
        self.accept("mouse3-up", self.mouse_click)


        # Keyboard Binds
        self.accept("a", updateKeyMap, ["left", True])
        self.accept("a-up", updateKeyMap, ["left", False])
        self.accept("d", updateKeyMap, ["right", True])
        self.accept("d-up", updateKeyMap, ["right", False])
        self.accept("w", updateKeyMap, ["up", True])
        self.accept("w-up", updateKeyMap, ["up", False])
        self.accept("s", updateKeyMap, ["down", True])
        self.accept("s-up", updateKeyMap, ["down", False])

        self.accept("space", updateKeyMap, ["rotate", True])
        self.accept("space-up", updateKeyMap, ["rotate", False])

        self.speed = 4
        self.angle = 0

        self.taskMgr.add(self.updateTask, "update")

    def mouse_click(self): 
        # mb = self.win.getPointer(0) 
        # print(mb.getX(), mb1.getY()) # range determined by resolution

        mouse_button = self.mouseWatcherNode.getMouse() # range is -1 to 1
        print(mouse_button.getX(), mouse_button.getY())

    def updateTask(self, task):
        dt = globalClock.getDt() # type: ignore

        pos = self.jack.getPos()

        # md = self.win.getPointer(0)
        # print(mb.getX(), mb.getY()) # range determined by resolution

        #if self.mouseWatcherNode.hasMouse(): # range is -1 to 1
         #   x = self.mouseWatcherNode.getMouseX()
          #  y = self.mouseWatcherNode.getMouseY()
           # print(x,y)
        
        if keyMap["left"]:
            pos.x -= self.speed * dt
        if keyMap["right"]:
            pos.x += self.speed * dt
        if keyMap["up"]:
            pos.z += self.speed * dt
        if keyMap["down"]:
            pos.z -= self.speed * dt
        if keyMap["rotate"]:
            self.angle += 1
            self.jack.setH(self.angle)
            
        

        self.jack.setPos(pos)
    
        return task.cont
    
game = GameWindow()
game.run()
