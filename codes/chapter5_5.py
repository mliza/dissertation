import pickle
import os
import haot
import molmass
import matplotlib.pyplot as plt
import scipy.constants as s_consts
import IPython


if __name__ == "__main__":
    input_pickle_path = "../resultsCFD/LES/openFoam/LES.pickle"

    # Loading pickle file
    file = open(input_pickle_path, 'rb')
    data_in = pickle.load(file)
    file.close()

    # Calculate Index of Refraction
    # Data[key][time,x_position,y_position]

    # Air polarizability
    t_axis = 1
    x_axis = 2
    y_axis = 50
    # CLEAN ME UP
    pol_kerl_air_m3 = haot.kerl_polarizability_temperature(data_in['T'], 'Air',
                                                        533) #[m^3]

    pol_kerl_air_SI = haot.polarizability_cgs_to_si(pol_kerl_air_m3 * 1e6)


    molar_mass_air = (0.78 * molmass.Formula('O2').mass + 0.21 *
                    molmass.Formula('N2').mass + 0.01 *
                      molmass.Formula('Ar').mass)
                    
    molar_density_air = data_in['rho'] * s_consts.N_A / molar_mass_air * 1e3

    n = 1/ (2 * s_consts.epsilon_0) * molar_density_air * pol_kerl_air_SI
    
    IPython.embed(colors = 'Linux')
    #haot.mass_density_to_molar_density(data_in['rho'],  )

