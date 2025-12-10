from panda3d.core import loadPrcFile, Loader, AmbientLight, DirectionalLight
loadPrcFile("Configs/config.prc")

from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor

filepath = "Character.glb" 

class GameWindow(ShowBase):
    loader: Loader # Explicit type definition for loader
    
    def __init__(self):
        super().__init__()

        # Load the model directly
        character = self.loader.loadModel(filepath)
        self.actor = Actor(character)
        self.actor.reparentTo(self.render)
        self.actor.setPos(0, 50, 3)
        self.actor.setScale(2, 2, 2)

        # Add lighting
        aLight = AmbientLight("ambient")
        aLight.setColor((0.5, 0.5, 0.5, 1))
        aLightNP = self.render.attachNewNode(aLight)
        self.render.setLight(aLightNP)

        dLight = DirectionalLight("directional")
        dLight.setColor((1, 1, 1, 1))
        dLightNP = self.render.attachNewNode(dLight)
        dLightNP.setHpr(45, -45, 0)
        self.render.setLight(dLightNP)

        # Show available animation tracks
        anim_names = self.actor.getAnimNames()
        print("Animations:", anim_names)

        # Play the first animation
        if anim_names:
            self.actor.loop("(Sitting) Walk")

        env = self.loader.loadModel("models/environment")
        env.reparentTo(self.render)

game = GameWindow()
game.run()
