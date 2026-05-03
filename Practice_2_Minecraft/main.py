from direct.showbase.ShowBase import ShowBase
from panda3d.core import DirectionalLight, AmbientLight

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        grassBlock = loader.loadModel('assets/glb/grass-block.glb')
        grassBlock.reparentTo(render)
        
        dLight = DirectionalLight('directional Light')
        dLightNodePath = render.attachNewNode(dLight)
        dLightNodePath.setHpr(30, -60, 0)
        render.setLight(dLightNodePath)

        aLight = AmbientLight('ambient Light')
        aLight.setColor((0.2, 0.2, 0.2, 1))
        aLightNodePath = render.attachNewNode(aLight)
        render.setLight(aLightNodePath)

game = Game()
game.run()
