import math
from ansys.aedt.core import Hfss

hfss = Hfss()
length_units = "m"
d = 0.04
w = 3/280
for n in range (1, 17):
    r = math.sqrt((n*w/4)**2+(n*d*w/4))
    hfss["r"+str(n)] = r

rings = []
delete = []
k = math.sqrt(3.1496)
tf = w/(4*(k-1))
for i in range(0, 4):
    hfss["h" + str(i)] = i*tf + 0.001
rings.append(hfss.modeler.create_cylinder(orientation = "XY", 
                                          origin = (0, 0, 0), 
                                          radius = "r"+str(1), 
                                          height = ("h" + str(3)), 
                                          name = "h" + str(1), 
                                          material="Plastic, PLA"))
for n in range(2, 17):
    i = (16-n)%4
    rings.append(hfss.modeler.create_cylinder(orientation = "XY", 
                                              origin = (0, 0, 0), 
                                              radius = "r"+str(n), 
                                              height = ("h" + str(i)), 
                                              name = "h" + str(n), 
                                              material="Plastic, PLA",
                                              num_sides= 20))
    delete.append(hfss.modeler.create_cylinder(orientation = "XY", 
                                               origin = (0, 0, 0), 
                                               radius = "r"+str(n-1), 
                                               height = ("h" + str(i)), 
                                               name = "delete" + str(n), 
                                               num_sides=20))
    rings[n-1].subtract(delete[n-2])
    hfss.modeler["delete"+str(n)].delete()
