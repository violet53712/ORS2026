import os
import tempfile
import time

from ansys.aedt.core import Hfss
# -

# ### Define constants
# Constants help ensure consistency and avoid repetition throughout the example.

AEDT_VERSION = "2024.2"
NUM_CORES = 4
NG_MODE = False  # Open AEDT UI when it is launched.
freq_range = ["1GHz", "5GHz"]

hfss = Hfss(version = AEDT_VERSION)
setup = hfss.create_setup(name="MySetup", setup_type = "HFSSDriven", Frequency = "3GHz")

setup.create_linear_step_sweep(
    unit="GHz",
    name="Sweep1",
    start_frequency=1,
    stop_frequency=5,
    step_size = 0.2,
    sweep_type="Interpolating",)
hfss.analyze()
hfss.post.create_report("db(S11)")

hfss.save_project()
hfss.release_desktop()
