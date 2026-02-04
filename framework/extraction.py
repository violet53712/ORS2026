from ansys.aedt.core import Hfss

def extract_s11(hfss):
    # Extract S-parameters

# variations = hfss.available_variations.nominal_values
# variations["Freq"] = [center_freq]
# variations["Theta"] = ["All"]
# variations["Phi"] = ["All"]
    report1 = hfss.post.create_report(expressions = "db(S11)", 
                                      variations = {"d": ["All"], "dw": ["All"], "w_inset": ["All"], "w": ["All"]}, 
                                      report_category = "Terminal Solution Data", 
                                      plot_type = "Rectangular Plot", 
                                      plot_name = "patch28s11")
    hfss.post.export_report_to_file( output_dir = "C:\\Users\\cli893\\Downloads\\ORS2026\\ml",
                                     plot_name = "patch28s11",
                                       extension = ".csv")
    print("Results extracted and saved to CSV.")
    return report1

def extract_gain(hfss):
    report2 = hfss.post.create_report(expressions = "db(RealizedGainPhi)", 
                                      variations = {"d": ["All"], "dw": ["All"], "w_inset": ["All"], "w": ["All"]}, 
                                      primary_sweep_variable = "Theta", 
                                      report_category = "Far Fields", 
                                      plot_type = "Radiation Pattern", 
                                      context = "Infinite Sphere1",
                                      plot_name = "patch28gain2")
    print(report2.plot_name)
    hfss.post.export_report_to_file( output_dir = "C:\\Users\\cli893\\Downloads\\ORS2026\\ml",
                                     plot_name = report2.plot_name, 
                                     extension = ".csv")
    print("Results extracted and saved to CSV.")
    return report2


#create_report(expressions=None, domain='Sweep', 
#              variations=None, primary_sweep_variable=None, 
#            secondary_sweep_variable=None, report_category=None,
#                plot_type='Rectangular Plot', context=None, 
#                subdesign_id=None, polyline_points=1001, 
#                name=None, sweep=None)