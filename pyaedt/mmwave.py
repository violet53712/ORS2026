aedt_process_id = "15688"
version = "2024.2"
print("Loading the PyAEDT Console.")

if version > "2023.1":
    from ansys.aedt.core import Desktop
    from ansys.aedt.core import settings

    settings.use_grpc_api = True
else:
    from pyaedt import Desktop
    from pyaedt import settings

    settings.use_grpc_api = False

desktop = Desktop(
    specified_version=version,
    aedt_process_id=aedt_process_id,
    new_desktop_session=False,
    non_graphical=False,
    close_on_exit=False,
    student_version=False,
)
from ansys.aedt.core import Hfss

hfss = Hfss()
hfss["ls"] = "30.176mm"
hfss["h"] = "1mm"
hfss["w"] =	"3.26025mm"
hfss["l"] =	"2.03049mm"	  
hfss["w_s"] = "50mm"	 
hfss["l_s"]	= "50mm"
hfss["h_s"]	= "50mm"	 
hfss["dw"] = "1mm"	 
hfss["d"] = "0.391"	 
hfss["w_inset"]	= "0.3mm"	 
hfss["l_inset"]	= "0.6mm"	 
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
                                     sizes = ["dw", "d*l"],
                                     name = "cutout")
feedline = hfss.modeler.create_rectangle(orientation = "XY",
                                     origin = ["-w_inset/2" ,"-l/2 + d*l - l_inset" ,0],
                                     sizes = ["w_inset", "l_inset"],
                                     name = "feedline")
patch.subtract(cutout)
patch.unite(feedline)

ground = hfss.modeler.create_rectangle(orientation = "XY",
                                     origin = ["-w_s/2" ,"-l_s/2" ,0],
                                     sizes = ["w_s", "l_s"],
                                     name = "ground")
feed = hfss.modeler.create_rectangle(orientation = "XZ",
                                     origin = ["-w_inset/2" ,"-l/2 + d*l - l_inset" ,0],
                                     sizes = ["-h", "w_inset"],
                                     name = "feed")

perfE1 = hfss.assign_perfecte_to_sheets("patch")
perfE2 = hfss.assign_perfecte_to_sheets("ground")
rad = hfss.assign_radiation_boundary_to_objects("air")

#port1 = hfss.lumped_port(
#    assignment="patch",
#    reference="ground",
#    create_port_sheet=True,
#    port_on_plane=True,
#    ,#[[0, "-l/2 + d - l_inset", "-h"],[0, "-l/2 + d - l_inset", 0]], 
#    impedance=50,
#    name="port1",
#    renormalize=True,
#    deembed=False,
#    terminals_rename=True
#)
port1 = hfss.lumped_port(
    assignment = "feed",
    reference = "patch",
    integration_line= hfss.AxisDir.ZPos, #[["0mm","-24.2413045150532mm","-1mm"],["0mm","-24.2413045150532mm",0]]
    #[[0, "-l/2 + d - l_inset", "-h"],[0, "-l/2 + d - l_inset", 0]], #hfss.AxisDir.ZPos,
    impedance = 50,
    name = "port1",
    renormalize = True,)


setup = hfss.create_setup(name="MySetup", setup_type = "HFSSDriven", Frequency = "3GHz")
setup.props["MaximumPasses"] = 10
setup.create_linear_step_sweep(
    unit="GHz",
    name="Sweep1",
    start_frequency=1,
    stop_frequency=5,
    step_size = 0.1,
    sweep_type="Interpolating",)
hfss.analyze()

hfss.post.create_report("db(S11)")

opt = hfss.optimizations

v = ["d", "dw", "w_inset", "l_inset"]

opt.add(calculation="dB(S(1,1))", variables = v, ranges={"Freq": ("4.3GHz", "4.5GHz")}, condition="<=",goal_value = "-20")

hfss.analyze()
ffdata = hfss.get_antenna_data(setup=hfss.nominal_adaptive, sphere="Infinite Sphere1")
ffdata.farfield_data.plot_cut(
    quantity="RealizedGain_Theta",
    primary_sweep="theta",
    title="co",
    quantity_format="dB10",
    is_polar = True,
)

ffdata.farfield_data.plot_cut(
    quantity="RealizedGain_Phi",
    primary_sweep="theta",
    secondary_sweep_value = 0,
    title="cross",
    quantity_format="dB10",
    is_polar = True,
)

hfss.save_project()
#hfss.release_desktop()