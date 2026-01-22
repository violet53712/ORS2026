from ansys.aedt.core import Hfss

hfss = Hfss()
hfss["ls"] = "10mm"
hfss["h"] = "0.3mm"
hfss["w"] =	"3.13475998969076mm"
hfss["l"] =	"2.42444930665735mm"	 
hfss["w_s"] = "50mm"	 
hfss["l_s"]	= "50mm"
hfss["h_s"]	= "50mm"
hfss["dw"] = "0.847852902077836mm"	 
hfss["d"] = "0.31872271467571mm"	 
hfss["w_inset"]	= "0.344836594189614mm"	 
hfss["l_inset"]	= "1.43026031668154mm"	 
hfss["dist"]	= "-40mm"	 
length_units = "mm"
freq_units = "GHz"
#(0.31872271467571, 0.847852902077836, 0.3, 10.0, 2.42444930665735, , 10.0, 10.0, 3.13475998969076, 0.344836594189614, 10.0)
d = 0.04
hfss.modeler.model_units = length_units

box = hfss.modeler.create_box(origin=["-w_s/10" ,"-l_s/10" , "dist"],
                              sizes=["w_s/5", "l_s/5", "-h"],
                              name="substrate",
                              material="FR4_epoxy")
air = hfss.modeler.create_box(origin=["-w_s" ,"-l_s" ,"-h_s/2 + dist"],
                              sizes=["2*w_s", "2*l_s", "2*h_s"],
                              name="air",
                              material="vacuum")
patch = hfss.modeler.create_rectangle(orientation = "XY",
                                     origin = ["-w/2" ,"-l/2" ,"dist"],
                                     sizes = ["w", "l"],
                                     name = "patch")
cutout = hfss.modeler.create_rectangle(orientation = "XY",
                                     origin = ["-dw/2" ,"-l/2" ,"dist"],
                                     sizes = ["dw", "d"],
                                     name = "cutout")
feedline = hfss.modeler.create_rectangle(orientation = "XY",
                                     origin = ["-w_inset/2" ,"-l/2 + d - l_inset" ,"dist"],
                                     sizes = ["w_inset", "l_inset"],
                                     name = "feedline")
patch.subtract(cutout)
patch.unite(feedline)

ground = hfss.modeler.create_rectangle(orientation = "XY",
                                     origin = ["-w_s/2" ,"-l_s/2" ,"-h+dist"],
                                     sizes = ["w_s", "l_s"],
                                     name = "ground")
feed = hfss.modeler.create_rectangle(orientation = "XZ",
                                     origin = ["-w_inset/2" ,"-l/2 + d - l_inset" ,"dist"],
                                     sizes = ["-h", "w_inset"],
                                     name = "feed")
hfss.modeler["cutout"].delete()

perfE1 = hfss.assign_perfecte_to_sheets("patch")
perfE2 = hfss.assign_perfecte_to_sheets("ground")
rad = hfss.assign_radiation_boundary_to_objects("air")

port1 = hfss.lumped_port(
     assignment = "feed",
     reference = "patch",
     integration_line= hfss.AxisDir.ZPos, #[["0mm","-24.2413045150532mm","-1mm"],["0mm","-24.2413045150532mm",0]]
     #[[0, "-l/2 + d - l_inset", "-h"],[0, "-l/2 + d - l_inset", 0]], #hfss.AxisDir.ZPos,
     impedance = 50,
     name = "port1",
     renormalize = False,)
