import pickle
import os
import haot
import matplotlib.pyplot as plt
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
    pol_kerl_air = haot.kerl_polarizability_temperature(data_in['T'], 'Air', 533)

    IPython.embed(colors = 'Linux')
