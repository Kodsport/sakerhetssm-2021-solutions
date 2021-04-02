# Sätt kameran mellan vänster, bottom och front-facet så kan man se flaggan
import vedo
import numpy as np

from PIL import Image

a = Image.open("/Users/jonathanloov/Documents/Projekt/Programmering/Projekt/sakerhetssm-2021/kval/forensics-anamorfos/chall.png")

d = np.array(a)

dd = d.reshape(-1, 3)

pts = vedo.Points(dd)

vedo.show(
    pts,
    at=0,
    N=0,
    axes=5,
    interactive=True,
    camera={
        "focalPoint": [128, 128, 128], "pos": [128 * 100, 0, 0], "parallelScale": 10,
        "viewAngle": 60,
    },
)
