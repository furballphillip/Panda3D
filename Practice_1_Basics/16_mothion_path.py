from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData
from direct.directutil import Mopath
from direct.interval.MopathInterval import *
from direct.filter.CommonFilters import CommonFilters

configVars = """
win-size 1280 720
show-frame-rate-meter 1
"""

loadPrcFileData("", configVars)

class MyGame(ShowBase):
    def __init__(self):
        super().__init__()
        self.set_background_color(0, 0, 0, 1)
        self.cam.setPos(0, -80, 0)

        self.light_model = self.loader.loadModel('models/misc/sphere')
        self.light_model.setScale(0.5)
        self.light_model.reparentTo(self.render)

        my_curve = Mopath.Mopath()
        my_curve.loadFile('assets/models/egg/curvey')

        my_interval = MopathInterval(my_curve, self.light_model, duration=10, name="mopath-curve")
        my_interval.loop()

        filters = CommonFilters(self.win, self.cam)
        filters.setBloom(size="medium")

        print(f"Number of knots: {my_curve.xyzNurbsCurve.getNumKnots()}")
        print(f"Knots: {my_curve.xyzNurbsCurve.getKnots()}")
        print(f"Order: {my_curve.xyzNurbsCurve.getOrder()}")
        print(f"Control vertices: {my_curve.xyzNurbsCurve.getCvs()}")


game = MyGame()
game.run()
