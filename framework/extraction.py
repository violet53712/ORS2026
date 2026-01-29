from ansys.aedt.core import Hfss

def extract_s11(hfss):
    # Extract S-parameters

    report1 = hfss.post.create_report(expressions = "db(S11)", variations = None, report_category = "Terminal Solution Data", plot_type = "Rectangular Plot", plot_name = "patch28")
    hfss.post.export_report_to_file( output_dir = "C:\\Users\\cli893\\Downloads\\ORS2026\\ml", plot_name = "patch28", extension = ".csv")
    print("Results extracted and saved to CSV.")
    return report1

def extract_gain(hfss):
    # Extract S-parameters
    # ffdata = hfss.get_antenna_data(setup=hfss.nominal_adaptive, sphere="Infinite Sphere1")
    # reportf = hfss.post.create_report(expressions = "db(GainPhi)", variations = None, report_category = "Far Fields Report", plot_type = "Rectangular Plot", plot_name = "patch28")
    # ffdata.farfield_data.plot_cut(
    # quantity="RealizedGain_Theta",
    # primary_sweep="theta",
    # title="co",
    # quantity_format="dB10",
    # is_polar = True,)
    report2 = hfss.post.create_report(expressions = "db(GainPhi)", primary_sweep_variable = "Theta", report_category = "Far Fields", plot_type = "Radiation Pattern", plot_name = "patch28")
    hfss.post.export_report_to_file( output_dir = "C:\\Users\\cli893\\Downloads\\ORS2026\\ml", plot_name = "patch28", extension = ".csv")
    print("Results extracted and saved to CSV.")
    return report2


#create_report(expressions=None, domain='Sweep', 
#              variations=None, primary_sweep_variable=None, 
#            secondary_sweep_variable=None, report_category=None,
#                plot_type='Rectangular Plot', context=None, 
#                subdesign_id=None, polyline_points=1001, 
#                name=None, sweep=None)