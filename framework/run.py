from ansys.aedt.core import Hfss
from ansys.aedt.core import Desktop
from ansys.aedt.core import settings
import generatepatch
import extraction

settings.use_grpc_api = True
version = "2024.2"
print("Loading the PyAEDT Console.")

desktop = Desktop(
    specified_version=version,
    new_desktop_session=False,
    non_graphical=False,
    close_on_exit=False,
    student_version=False,
)


hfss = Hfss(solution_type="HFSS with Hybrid and Arrays")
hfss.hybrid = True

generatepatch.generate_patch(hfss)
generatepatch.generate_lens(hfss)
generatepatch.generate_febi(hfss)
setup = hfss.create_setup(name="MySetup", setup_type = "HFSSDriven", Frequency = "28GHz")
setup.props["MaximumPasses"] = 20

#generatepatch.analysis_setup(hfss, False, setup)
generatepatch.analysis_setup(hfss, True, setup)

#generatepatch.optimization_s11_setup(hfss,["dw", "w_inset","d", "w"])
#generatepatch.optimization_gain_setup(hfss,["dw", "w_inset","d", "w"])
hfss.analyze()

#r1 = extraction.extract_s11(hfss)
#r2 = extraction.extract_gain(hfss)



