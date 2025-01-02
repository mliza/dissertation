import pickle
import os
import haot
import molmass
import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as s_consts
import IPython

def plot_OPL( ):
    pass

def plot_OPD( ):
    pass

def plot_index_of_refraction(n_index, data_in, fig_config, ploting_path):
    # Axis where to plot
    [t_axis, x_axis, y_axis] =  fig_config["data_shape"]
    time_val = data_in["time_s"][t_axis] 
    time_pdf = str(time_val).replace('.', '_')


    for x, val in enumerate(data_in['spacing_dx']):
        plt.plot((n_index['dilute'][t_axis, x, :] - 1) * 1e3, data_in['Y'][t_axis, x],
                linewidth=fig_config['line_width'], 
                label=f'X = {val} $[cm]$ at {time_val} $[s]$') 

    plt.legend(fontsize=fig_config["legend_size"])
    plt.xlabel("(n - 1) $\\times 10^{-3}[ ]$", fontsize=fig_config["axis_label_size"])
    plt.ylabel("Y $[cm]$", fontsize=fig_config["axis_label_size"])
    plt.xticks(fontsize=fig_config['ticks_size'])
    plt.yticks(fontsize=fig_config['ticks_size'])

    plt.savefig(
        os.path.join(ploting_path, f"lesRefractiveIndex_time{time_pdf}.pdf"),
        format="pdf",
        bbox_inches="tight",
        dpi=600,
    )
    plt.close()

if __name__ == "__main__":
    input_pickle_path = "../resultsCFD/LES/openFoam/LES.pickle"
    ploting_path = "../figures/chapter5/lesStudy"


    # Figure configuration
    fig_config = {}
    fig_config["line_width"] = 3
    fig_config["fig_width"] = 6
    fig_config["fig_height"] = 5
    fig_config["dpi_size"] = 600
    fig_config["ticks_size"] = 14
    fig_config["legend_size"] = 11
    fig_config["axis_label_size"] = 14
    fig_config['ticks_size'] = 13
    fig_config["title_size"] = 18


    # Loading pickle file
    file = open(input_pickle_path, 'rb')
    data_in = pickle.load(file)
    file.close()

    # Calculate Index of Refraction
    # Data[key][time,x_position,y_position]

    # Air polarizability
    t_axis = 36
    x_axis = 2
    y_axis = 50
    fig_config["data_shape"] = [t_axis, x_axis, y_axis]

    index_refraction = haot.index_of_refraction_density_temperature(data_in['T'],
                                                   data_in['rho'], 'Air', 633)
    [time, x_elements, y_elements] = np.shape(data_in['Y'])


    tmp = np.zeros([time, x_elements, y_elements])
    if np.min(data_in['Y']) < 0: 
        for t in range(time):
            for x in range(x_elements):
                tmp[t,x] = data_in['Y'][t,x,:] - min(data_in['Y'][t,x,:])

    # Check OPL
    opl_dict = haot.optical_path_length(index_refraction, tmp)
    plot_index_of_refraction(index_refraction, data_in, fig_config,
                             ploting_path)

