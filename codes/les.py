import pickle
import haot
import IPython
import os
import numpy as np
import figure_configurations
from matplotlib.ticker import FormatStrFormatter
import matplotlib.pyplot as plt

def plot_OPD_3D(x_range, y_range, OPD, OPL_mean, flag_Z='Y'):
    fig_config = figure_configurations.figure_settings()
    fig_config['fig_saving'] = ('/Users/martin/Documents/Schools/UoA/supplement/figures')
    X, Y = np.meshgrid(y_range, x_range)
    fig = plt.figure(figsize=(fig_config["fig_width"], fig_config["fig_height"]))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(X, Y, OPD, 
                           label=fr'$\overline{{OPL}} = {OPL_mean:0.3}$',
                           cmap="turbo", edgecolor="none")


    if flag_Z == 'Z':
        ax.set_xlabel("Z $[cm]$", fontsize=fig_config["axis_label_size"])
        ax.set_zlabel("$OPD_{xz}$ $[m m]$", labelpad=20,
                      fontsize=fig_config["axis_label_size"])


    if flag_Z == 'Y':
        ax.set_xlabel("Y $[mm]$", fontsize=fig_config["axis_label_size"])
        ax.set_zlabel("$OPD_{xy}$ $[m m]$", labelpad=20,
                      fontsize=fig_config["axis_label_size"])

    ax.set_ylabel("X $[cm]$", fontsize=fig_config["axis_label_size"])

    # Fix z-axis formatting
    ax.zaxis.get_major_formatter().set_useOffset(False)
    ax.zaxis.set_major_formatter(FormatStrFormatter("%.4f"))
    plt.legend(fontsize=fig_config["legend_size"])

    #plt.show()
    if flag_Z == 'Z':
        plt.savefig(
            os.path.join(fig_config["fig_saving"], f"OPD_XZ.pdf"),
            format="pdf",
        )

    if flag_Z == 'Y':
        plt.savefig(
            os.path.join(fig_config["fig_saving"], f"OPD_XY.pdf"),
            format="pdf",
        )
    plt.close()

def plot_OPL_3D(x_range, y_range, OPL_xy, flag_Z='Y'):
    OPL_std = np.mean(np.std(OPL_xy))
    fig_config = figure_configurations.figure_settings()
    fig_config['fig_saving'] = ('/Users/martin/Documents/Schools/UoA/supplement/figures')
    X, Y = np.meshgrid(y_range, x_range)
    fig = plt.figure(figsize=(fig_config["fig_width"], fig_config["fig_height"]))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(X, Y, OPL_xy, label=f'$\sigma_x$={OPL_std:0.3}',
                           cmap="turbo", edgecolor="none")

    if flag_Z == 'Z':
        ax.set_xlabel("Z $[cm]$", fontsize=fig_config["axis_label_size"])
        ax.set_zlabel("$OPL_{xz}$ $[mm]$", 
                   labelpad=20,
                   fontsize=fig_config["axis_label_size"])
    if flag_Z == 'Y':
        ax.set_xlabel("Y $[mm]$", fontsize=fig_config["axis_label_size"])
        ax.set_zlabel("$OPL_{xy}$ $[mm]$", 
                   labelpad=20,
                   fontsize=fig_config["axis_label_size"])

    ax.set_ylabel("X $[cm]$", fontsize=fig_config["axis_label_size"])


    # Fix z-axis formatting
    ax.zaxis.get_major_formatter().set_useOffset(False)
    ax.zaxis.set_major_formatter(FormatStrFormatter("%.4f"))
    plt.legend(fontsize=fig_config["legend_size"])

    #plt.show()

    if flag_Z == 'Z':
        plt.savefig(
            os.path.join(fig_config["fig_saving"], f"OPL_XZ.pdf"),
            format="pdf",
        )
    if flag_Z == 'Y':
        plt.savefig(
            os.path.join(fig_config["fig_saving"], f"OPL_XY.pdf"),
            format="pdf",
        )
    plt.close()


def gladstone_kerl_approximation(temperature_K, mass_density, wavelength_nm):
    pol_kerl_air_m3 = haot.kerl_polarizability_temperature(data['T'], "Air", wavelength_nm)
    pol_kerl_SI = haot.polarizability_cgs_to_si(pol_kerl_air_m3 * 1e6)
    IPython.embed(colors = 'Linux')
    #TODO: Calculate GD




def main(data_in):
    wavelength_nm = 633
    index = haot.index_of_refraction_density_temperature(data['T'], data['RHO'], "Air",
                                                 wavelength_nm)
    gd_kerl = gladstone_kerl_approximation(data['T'], data['RHO'], wavelength_nm):
    gd_air = gladstone_dale_air_wavelength(633.0)

    x_00 = data['X'][:,0,0]
    y_00 = data['Y'][0,:,0]
    z_00 = data['Z'][0,0,:] - data['Z'][0,0,:][0]

    ## TODO: Plot GD and Index ##

    # Index average on z
    x_range, y_range, z_range = np.shape(index['dilute'])
    OPL_xy = np.empty([x_range, y_range])
    OPL_xz = np.empty([x_range, z_range])

    # Calculate OPL as a function of xy 
    for i in range(x_range):
        for j in range(y_range):
            OPL_xy[i,j] = haot.optical_path_length(index['dilute'][i,j,:],
                                                   z_00)
        for k in range(z_range):
            OPL_xz[i,k] = haot.optical_path_length(index['dilute'][i,:,k],
                                                   y_00)

    # OPD_x = average on x, OPD_y = average on y
    OPD_xy = OPL_xy - np.mean(OPL_xy)
    OPD_xz = OPL_xz - np.mean(OPL_xz)

    # Plots ##
    """
    plot_OPL_3D(x_00 * 1E2, data['Z'][0,0,:] * 1E2, OPL_xz * 1E3, flag_Z='Z')
    plot_OPL_3D(x_00 * 1E2, data['Y'][0,:,0] * 1E3, OPL_xy * 1E3, flag_Z ='Y')
    plot_OPD_3D(x_00 * 1E2, data['Y'][0,:,0] * 1E3, OPD_xy * 1E3,
                np.mean(OPL_xy), flag_Z='Y')
    plot_OPD_3D(x_00 * 1E2, data['Z'][0,0,:] * 1E2, OPD_xz * 1E3,
                np.mean(OPL_xz), flag_Z='Z')
    """
    # Plots ##



if __name__ == "__main__":
    data_path = ('/Users/martin/Documents/Research/UoA/Projects/LLNL/dns_analysis/plate_data/data_15/pickle')
    with open(os.path.join(data_path,'dict_3D.pickle'), "rb") as f:
        data = pickle.load(f)

    main(data)

