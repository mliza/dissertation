import os
import haot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import IPython


def read_paper_data(paper_data):
    files_in = os.listdir(paper_data)
    dict_out = { }
    for i in files_in:
        key = i.split('.')[0]
        df_in = pd.read_csv(os.path.join(paper_data, i))
        dict_out[key] = df_in.to_dict(orient='list')
    return dict_out

def calculate_buldakov_pol():
    molecule = ['H2', 'N2', 'O2']
    temperature_K = np.arange(100, 1500 + 50, 50)
    vibrational_number = 1 
    rotational_number = 2
    vib_axis = range(vibrational_number + 1)
    rot_axis = range(rotational_number + 1)
    buldakov_dict = { }
    buldakov_dict['temperature_K'] = temperature_K







if __name__ == "__main__":
    # Loading Paper Data
    budakovData = read_paper_data("buldakovPaper")
    tropinaData = read_paper_data("tropinaPaper")
    kerlData = read_paper_data("kerlPaper")

    IPython.embed(colors = 'Linux')
    """ 
    plt.plot(budakovData['buldakov_O2']['temperature_K'],
    budakovData['buldakov_O2']['polarizability_m3']*1E6, label='Buldakov O2')

    plt.plot(kerlData['kerl_O2']['temperature_K'],
    kerlData['kerl_O2']['polarizability_m3']*1E6, label='Kerl O2')

    plt.legend()
    plt.xlabel("Temperature $[K]$)
    plt.ylabel("Polarizability $[cm^3]$)

    """
