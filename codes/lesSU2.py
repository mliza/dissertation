import haot
import os
import matplotlib.pyplot as plt
import IPython
import pyvista as pv
import figure_configurations as fig_conf
import scipy.constants as s_consts
import molmass

def calculate_optics(mesh, wavelength_nm):
    cell_data = mesh.point_data_to_cell_data()

        # HAOT
    index_of_refraction = haot.index_of_refraction_density_temperature(cell_data["Temperature"],
                                                     cell_data["Density"],
                                                     "Air", wavelength_nm)
    mesh.cell_data["index_dilute"] = index_of_refraction["dilute"]
    mesh.cell_data["index_dense"] = index_of_refraction["dense"]

    kerl_polarizability_m3 = haot.kerl_polarizability_temperature(cell_data["Temperature"], "Air",
                                         wavelength_nm)
    gd_constant = haot.air_gladstone_dale_polarizability(kerl_polarizability_m3)

    mesh.cell_data["kerl_polarizability"] = kerl_polarizability_m3
    mesh.cell_data["gd_const"] = gd_constant

    del index_of_refraction



def main(vtu_path_in, time_in, fig_config):
    wavelength_nm = 633.0

    for i, val in enumerate(vtu_path_in[0:2]):
        # pyvista stuff
        reader = pv.get_reader(val)
        mesh = reader.read()

        # Optics
        calculate_optics(mesh, wavelength_nm)
        IPython.embed(colors = 'Linux')




if __name__ == "__main__":
    flow_path = "../resultsCFD/LES/LES_SU2/flow/"
    vtu_files = sorted(os.listdir(flow_path))
    time_in = sorted([int(k.split('.')[0].split('_')[1]) for k in vtu_files])
    vtu_path_in = sorted([os.path.join(flow_path, k) for k in vtu_files])
    fig_config = fig_conf.figure_settings()

    main(vtu_path_in, time_in, fig_config)


