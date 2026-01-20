from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData
from panda3d.core import OrthographicLens, TextureStage

configVars = """
win-size 1920 1080
show-frame-rate-meter True 
"""

loadPrcFileData("", configVars)

key_map = {
    "left": False,
    "right": False
}

def update_key_map(control_name, control_state, entity, walking):
    key_map[control_name] = control_state
    if key_map["left"] or key_map["right"]: # Check if movement key is pressed
        entity.find('**/+SequenceNode').node().loop(True, 0, 1)  # Walk: toggle between frames 0 and 1
    else:
        entity.find('**/+SequenceNode').node().loop(True, 0, 0)  # Idle: stay on frame 0

    if control_state:  # Only flip when key is pressed, not released
        if control_name == "left":
            entity.setTexScale(TextureStage.getDefault(), -1, 1)
        elif control_name == "right":
            entity.setTexScale(TextureStage.getDefault(), 1, 1)

class GameWindow(ShowBase):
    def __init__(self):
        super().__init__()
        self.loader : Loader # Explicit type definition for loader
        
        self.set_background_color(0.1, 0.1, 0.1, 1)

        self.knight = self.loader.loadModel("assets/texture_cards/Knight.egg")
        self.knight.setScale(3.0)
        self.knight.reparentTo(self.render)
        self.knight.setPos(0, 0, 0)
        self.knight.setP(-90)  # Pitch -90 degrees so the front of the plane faces the camera
        
        print(f"Knight loaded: {self.knight}")
        print(f"Knight position: {self.knight.getPos()}")
        print(f"Knight scale: {self.knight.getScale()}")
        
        #self.knight.find('**/+SequenceNode').node().loop(True, 10, 19)
        self.knight.find('**/+SequenceNode').node().loop(True, 0, 0)  # Start with idle on frame 0

        lens = OrthographicLens()
        lens.setFilmSize(20, 11.25)  # Shows a 20x11.25 unit area
        lens.setNearFar(-1000, 1000)
        self.cam.node().setLens(lens)
        self.cam.setPos(0, 5, 1)
        self.cam.lookAt(0, 5, 0)

        self.accept("arrow_left", update_key_map, ["left", True, self.knight, True])
        self.accept("arrow_left-up", update_key_map, ["left", False, self.knight, False])
        self.accept("arrow_right", update_key_map, ["right", True, self.knight, True])
        self.accept("arrow_right-up", update_key_map, ["right", False, self.knight, False])

        self.taskMgr.add(self.move_knight, "move-knight")

        self.x = 0
        self.speed = 10

    def move_knight(self, task):
        dt = globalClock.getDt()

        if key_map["left"]:
            self.x -= self.speed * dt
        if key_map["right"]:
            self.x += self.speed * dt

        self.knight.setPos(self.x, 0, 0)

        return task.cont
        
        
game = GameWindow()
game.run()
