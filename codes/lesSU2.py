import haot
import os
import matplotlib.pyplot as plt
import IPython
import pyvista as pv
import figure_configurations as fig_conf
import scipy.constants as s_const
import molmass

def air_gladstone_dale_density(polarizability: float):
    """
    Calculates the Air Gladstone Dale constant as a function of density. 

    Parameters:
        polarizability: polarizability [m3]

    Returns:
        Gladstone Dale constant in [m3/kg]
    """
    molar_mass_air_gmol = (
        0.78 * molmass.Formula("N2").mass
        + 0.21 * molmass.Formula("O2").mass
        + 0.01 * molmass.Formula("Ar").mass
    )
    molar_mass_air = molar_mass_air_gmol * 1e-3

    return (s_const.N_A * polarizability) / (2 * s_const.epsilon_0 *
                                             molar_mass_air)




def calculate_optics(cell_data, wavelength_nm):
        # HAOT
    #TODO: RUN THIS AGAIN
    index_of_refraction = haot.index_of_refraction_density_temperature(cell_data["Temperature"],
                                                     cell_data["Density"],
                                                     "Air", wavelength_nm)
    kerl_polarizability = haot.kerl_polarizability_temperature(cell_data["Temperature"], "Air",
                                         wavelength_nm)
    gd_constant = air_gladstone_dale_density(kerl_polarizability)
    IPython.embed(colors='Linux')

    # TODO: Calculate GD




def main(vtu_path_in, time_in, fig_config):
    wavelength_nm = 633.0

    for i, val in enumerate(vtu_path_in[0:2]):
        # pyvista stuff
        reader = pv.get_reader(val)
        mesh = reader.read()
        cell_data = mesh.point_data_to_cell_data()

        # Optics
        calculate_optics(cell_data, wavelength_nm)




if __name__ == "__main__":
    flow_path = "/Users/martin/Desktop/flow"
    vtu_files = sorted(os.listdir(flow_path))
    time_in = sorted([int(k.split('.')[0].split('_')[1]) for k in vtu_files])
    vtu_path_in = sorted([os.path.join(flow_path, k) for k in vtu_files])
    fig_config = fig_conf.figure_settings()

    main(vtu_path_in, time_in, fig_config)


