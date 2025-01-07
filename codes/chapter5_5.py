import pickle

import haot
import molmass
import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as s_consts
import IPython
import os



def plot_OPL(opl, data_in, fig_config,
             plotting_path):
    for x, val in enumerate(data_in['spacing_dx']):
        space_pdf = str(val).replace('.', '_')
        plt.plot(data_in['time_s'], opl[:, x],
                linewidth=fig_config['line_width'], 
                label=f'X = {val} $[cm]$') 

        plt.legend(fontsize=fig_config["legend_size"])
        plt.xlabel("Time $[s]$", fontsize=fig_config["axis_label_size"])
        plt.ylabel("OPL $[ ]$", fontsize=fig_config["axis_label_size"])
        plt.xticks(fontsize=fig_config['ticks_size'])
        plt.yticks(fontsize=fig_config['ticks_size'])

        plt.savefig(
            os.path.join(plotting_path, f"lesOPL_x{space_pdf}.pdf"),
            format="pdf",
            bbox_inches="tight",
            dpi=600,
        )
        plt.close()

def plot_OPL_3D(opl, data_in, fig_config, plotting_path):
    time = data_in['time_s']
    x_pos = data_in['spacing_dx']

    x_axis_mesh, time_mesh = np.meshgrid(data_in['spacing_dx'],
    data_in['time_s'])
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"},
                           figsize=(fig_config['fig_width'],
                            fig_config['fig_height']))

    surf = ax.plot_surface(x_axis_mesh, time_mesh, 
                           opl,
                           cmap='viridis', edgecolor='k',
                           alpha=0.8,
                           linewidth=0.5)

    #cont = ax.contour(x_axis_mesh, time_mesh, opl, zdir='z', offset = -0.001,
    #                  cmap='coolwarm')

    # Change grid and background colors
    ax.set_facecolor('white') 
    fig.patch.set_facecolor('white')
    ax.grid(False)

    # 3D axis views
    #ax.view_init(elev=elev_ang, azim=azim_ang)

    # Labels
    ax.set_xlabel('X distance # $[m]$',
                   fontsize=fig_config['axis_label_size'])

    ax.set_ylabel('Time # $[s]$',
                   fontsize=fig_config['axis_label_size'])

    ax.set_zlabel('OPL $[\;]$',
                   fontsize=fig_config['axis_label_size'])

    plt.show() 

def plot_OPD_3D(opd, data_in, fig_config, plotting_path):
    time = data_in['time_s']
    x_pos = data_in['spacing_dx']

    x_axis_mesh, time_mesh = np.meshgrid(data_in['spacing_dx'],
    data_in['time_s'])
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"},
                           figsize=(fig_config['fig_width'],
                            fig_config['fig_height']))

    surf = ax.plot_surface(x_axis_mesh, time_mesh, 
                           opd,
                           cmap='viridis', edgecolor='k',
                           alpha=0.8,
                           linewidth=0.5)

    cont = ax.contour(x_axis_mesh, time_mesh, opd, zdir='z', offset = -0.001,
                      cmap='coolwarm')

    # Change grid and background colors
    ax.set_facecolor('white') 
    fig.patch.set_facecolor('white')
    ax.grid(False)

    # 3D axis views
    #ax.view_init(elev=elev_ang, azim=azim_ang)

    # Labels
    ax.set_xlabel('X distance # $[m]$',
                   fontsize=fig_config['axis_label_size'])

    ax.set_ylabel('Time # $[s]$',
                   fontsize=fig_config['axis_label_size'])

    ax.set_zlabel('OPD $[\;]$',
                   fontsize=fig_config['axis_label_size'])

    plt.show() 


def plot_index_of_refraction(n_index, data_in, fig_config, plotting_path):
    # Axis where to plot
    [t_axis, x_axis, y_axis] =  fig_config["data_shape"]
    time_val = data_in["time_s"][t_axis] 
    time_pdf = str(time_val).replace('.', '_')
    spacing = data_in['spacing_dx'][0]
    dx_pdf = str(spacing).replace('.', '_')

    fig = plt.figure(figsize=(fig_config['fig_width'],
                              fig_config['fig_height']))

    for x, val in enumerate(data_in['spacing_dx'][:6]):
        plt.plot((n_index['dilute'][t_axis, x, :] - 1) * 1e3,
                 data_in['Y'][t_axis, x] * 1e2,
                linewidth=fig_config['line_width'], 
                 label=f'X = {val * 1e3:.1f} $[mm]$') 

    plt.legend(fontsize=fig_config["legend_size"])
    plt.xlabel("(n - 1) $\\times 10^{-3}[ ]$", fontsize=fig_config["axis_label_size"])
    plt.ylabel("Y $[cm]$", fontsize=fig_config["axis_label_size"])
    plt.xticks(fontsize=fig_config['ticks_size'])
    plt.yticks(fontsize=fig_config['ticks_size'])

    plt.savefig(
        os.path.join(plotting_path,
                     f"lesRefractiveIndex_time{time_pdf}_dx{dx_pdf}.pdf"),
        format="pdf",
        bbox_inches="tight",
        dpi=600,
    )
    plt.close()

if __name__ == "__main__":
    input_pickle_path = "../resultsCFD/LES/openFoam/LES_00.pickle"
    plotting_path = "results_test"
    plotting_path = "../figures/chapter5/lesStudy"


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

    # Data[key][time,x_position,y_position]

    # Air polarizability
    t_axis = 36
    x_axis = 2
    y_axis = 50
    fig_config["data_shape"] = [t_axis, x_axis, y_axis]

    # Calculate AO
    # -1 is required due to the meshing ignores the last element
    index_refraction = haot.index_of_refraction_density_temperature(data_in['T'][:-1],
                                                data_in['rho'][:-1], 'Air', 633)
    opl_dict = haot.optical_path_length(index_refraction, data_in['Y'][:-1], 2)
    opd_dict_t = haot.optical_path_difference(opl_dict, 0)

    #y_vector = [x,y], it changes based on X 
    y_vector = data_in['Y'][t_axis,:,:]
    n_ = index_refraction['dilute'][0,:,:]

    mesh_opl = np.zeros([len(data_in['spacing_dx']), len(y_vector[0,:])- 1])

    for x, val in enumerate(data_in['spacing_dx']):
        y_= np.linspace(np.min(y_vector[x,:]), np.max(y_vector[x,:]),
                        len(y_vector[x,:]))

        mesh_opl[x] = n_[x,:][:-1] * np.diff(y_) #[x, y]


    tot_opl_x = np.sum(mesh_opl, axis=1) #Sum on Y axis


    IPython.embed(colors = 'Linux')






    plot_index_of_refraction(index_refraction, data_in, fig_config,
                             plotting_path)





    # Plots #
    """

    plot_index_of_refraction(index_refraction, data_in, fig_config,
                             plotting_path)

    plot_OPD_3D(opd_dict_t['dilute'], data_in, fig_config, plotting_path)
    plot_OPL_3D(opl_dict['dilute'], data_in, fig_config,
                             plotting_path)


    #plot_OPD_3D(opd_dict_t['dense'], data_in, fig_config, plotting_path)
    """

