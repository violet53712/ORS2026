from ansys.aedt.core import Hfss
import generatepatch

hfss = Hfss()
generatepatch.generate_patch(hfss)

hfss.analyze()