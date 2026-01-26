from ansys.aedt.core import Hfss
from ansys.aedt.core import Desktop
from ansys.aedt.core import settings
import generatepatch

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


hfss = Hfss()

generatepatch.generate_patch(hfss)

generatepatch.analysis_setup(hfss, "Interpolating")

hfss.post.create_report("db(S11)")


hfss.analyze()
