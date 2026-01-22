from ansys.aedt.core import Hfss

hfss = Hfss()
hfss["ls"] = "30.176mm"
hfss["h"] = "1mm"
hfss["w"] =	"30.1511mm"
hfss["l"] =	"24.64mm"	 
hfss["t"] ="3mm"	 
hfss["w_s"] = "50mm"	 
hfss["l_s"]	= "50mm"
hfss["h_s"]	= "50mm"	 
hfss["dw"] = "9mm"	 
hfss["d"] = "8mm"	 
hfss["w_inset"]	= "3mm"	 
hfss["l_inset"]	= "20mm"	 
length_units = "mm"
freq_units = "GHz"
hfss.modeler.model_units = length_units

box = hfss.modeler.create_box(origin=["-w_s/2" ,"-l_s/2" , 0],
                              sizes=["w_s", "l_s", "-h"],
                              name="substrate",
                              material="FR4_epoxy")
air = hfss.modeler.create_box(origin=["-w_s" ,"-l_s" ,"-h_s"],
                              sizes=["2*w_s", "2*l_s", "2*h_s"],
                              name="air",
                              material="vacuum")
patch = hfss.modeler.create_rectangle(orientation = "XY",
                                     origin = ["-w/2" ,"-l/2" ,"0mm"],
                                     sizes = ["w", "l"],
                                     name = "patch")
cutout = hfss.modeler.create_rectangle(orientation = "XY",
                                     origin = ["-dw/2" ,"-l/2" ,"0mm"],
                                     sizes = ["dw", "d"],
                                     name = "cutout")
feedline = hfss.modeler.create_rectangle(orientation = "XY",
                                     origin = ["-w_inset/2" ,"-l/2 + d - l_inset" ,0],
                                     sizes = ["w_inset", "l_inset"],
                                     name = "feedline")
patch.subtract(cutout)
patch.unite(feedline)

ground = hfss.modeler.create_rectangle(orientation = "XY",
                                     origin = ["-w_s/2" ,"-l_s/2" ,"-h",0],
                                     sizes = ["w_s", "l_s"],
                                     name = "ground")
feed = hfss.modeler.create_rectangle(orientation = "XZ",
                                     origin = ["-w_inset/2" ,"-l/2 + d - l_inset" ,0],
                                     sizes = ["-h", "w_inset"],
                                     name = "feed")

perfE1 = hfss.assign_perfecte_to_sheets("patch")
perfE2 = hfss.assign_perfecte_to_sheets("ground")
rad = hfss.assign_radiation_boundary_to_objects("air")

#hfss["l_inset"]	= "11mm"	
#hfss.lumped_port(feed, feedline, hfss.AxisDir.Zpos, 50, "LumpedPort", True, False)

setup = hfss.create_setup(name="MySetup", setup_type = "HFSSDriven", Frequency = "3GHz")

setup.create_frequency_sweep(
    unit="GHz",
    name="Sweep1",
    start_frequency=1,
    stop_frequency=5,
    sweep_type="Interpolating",
)

hfss.save_project()