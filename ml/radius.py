import math

d = 0.04
w = 3/280
for n in range (1, 17):
    r = math.sqrt((n*w/4)**2+(n*d*w/4))
    print(r)

import math
from ansys.aedt.core import Hfss
hfss = Hfss()
length_units = "m"
d = 0.04
w = 3/280
for n in range (1, 17):
    r = math.sqrt((n*w/4)**2+(n*d*w/4))
    hfss["r"+str(n)] = r
    box = hfss.modeler.create_circle(origin=[0, 0 , 0],
                              radius = "r"+str(n),
                              name="ring"+str(n),
                              material="Plastic, PLA")