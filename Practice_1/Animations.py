from panda3d.core import loadPrcFile, Loader, AmbientLight, DirectionalLight
loadPrcFile("Configs/config.prc")

from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor

character_model_path = "Character.glb" 

class GameWindow(ShowBase):
    loader: Loader # Explicit type definition for loader
    
    def __init__(self):
        super().__init__()

        # Load the model directly
        character_model = self.loader.loadModel(character_model_path)
        self.character_actor = Actor(character_model)
        self.character_actor.reparentTo(self.render)
        self.character_actor.setPos(0, 50, 3)
        self.character_actor.setScale(2, 2, 2)

        # Add lighting
        ambient_light = AmbientLight("ambient")
        ambient_light.setColor((0.5, 0.5, 0.5, 1))
        ambient_light_np = self.render.attachNewNode(ambient_light)
        self.render.setLight(ambient_light_np)

        directional_light = DirectionalLight("directional")
        directional_light.setColor((1, 1, 1, 1))
        directional_light_np = self.render.attachNewNode(directional_light)
        directional_light_np.setHpr(45, -45, 0)
        self.render.setLight(directional_light_np)

        # Show available animation tracks
        animation_names = self.character_actor.getAnimNames()
        print("Animations:", animation_names)

        # Play the first animation
        if animation_names:
            self.character_actor.loop("(Sitting) Walk")

        environment_model = self.loader.loadModel("models/environment")
        environment_model.reparentTo(self.render)

game = GameWindow()
game.run()
