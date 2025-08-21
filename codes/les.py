import pickle
import haot
import IPython
import os
import numpy as np
import figure_configurations
from matplotlib.ticker import FormatStrFormatter
import matplotlib.pyplot as plt

def plot_OPD_3D(x_range, y_range, OPD):
    fig_config = figure_configurations.figure_settings()
    fig_config['fig_saving'] = ('/Users/martin/Documents/Schools/UoA/supplement/figures')
    X, Y = np.meshgrid(y_range, x_range)
    fig = plt.figure(figsize=(fig_config["fig_width"], fig_config["fig_height"]))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(X, Y, OPD, cmap="turbo", edgecolor="none")
    ax.set_ylabel("X $[cm]$", fontsize=fig_config["axis_label_size"])

    ax.set_xlabel("Z $[cm]$", fontsize=fig_config["axis_label_size"])
    ax.set_zlabel("$\\overline{OPD}_{xz}$ $[m m]$", labelpad=20,
                  fontsize=fig_config["axis_label_size"])

    #ax.set_xlabel("Y $[mm]$", fontsize=fig_config["axis_label_size"])
    #ax.set_zlabel("$\\overline{OPD}_{xy}$ $[m m]$", labelpad=20, fontsize=fig_config["axis_label_size"])

    # Fix z-axis formatting
    ax.zaxis.get_major_formatter().set_useOffset(False)
    ax.zaxis.set_major_formatter(FormatStrFormatter("%.4f"))

    #plt.show()
    plt.savefig(
        os.path.join(fig_config["fig_saving"], f"OPD_XZ.pdf"),
        #os.path.join(fig_config["fig_saving"], f"OPD_XY.pdf"),
        format="pdf",
        #bbox_inches="tight",
    )
    plt.close()
def plot_OPL_3D(x_range, y_range, OPL_xy):
    fig_config = figure_configurations.figure_settings()
    fig_config['fig_saving'] = ('/Users/martin/Documents/Schools/UoA/supplement/figures')
    X, Y = np.meshgrid(y_range, x_range)
    fig = plt.figure(figsize=(fig_config["fig_width"], fig_config["fig_height"]))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(X, Y, OPL_xy, cmap="turbo", edgecolor="none")
    #ax.set_xlabel("Z $[cm]$", fontsize=fig_config["axis_label_size"])
    ax.set_xlabel("Y $[mm]$", fontsize=fig_config["axis_label_size"])
    ax.set_ylabel("X $[cm]$", fontsize=fig_config["axis_label_size"])
    ax.set_zlabel("OPL $[mm]$", labelpad=20, fontsize=fig_config["axis_label_size"])

    # Fix z-axis formatting
    ax.zaxis.get_major_formatter().set_useOffset(False)
    ax.zaxis.set_major_formatter(FormatStrFormatter("%.4f"))

    #plt.show()
    plt.savefig(
        os.path.join(fig_config["fig_saving"], f"OPL_XZ.pdf"),
        #os.path.join(fig_config["fig_saving"], f"OPL_XY.pdf"),
        format="pdf",
        #bbox_inches="tight",
    )
    plt.close()

def main(data_in):
    index = haot.index_of_refraction_density_temperature(data['T'], data['RHO'], "Air",
                                                 633.0)
    x_00 = data['X'][:,0,0]
    y_00 = data['Y'][0,:,0]
    z_00 = data['Z'][0,0,:] - data['Z'][0,0,:][0]
    X, Y = np.meshgrid(x_00, y_00, indexing='ij')

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

    OPD_x = haot.optical_path_difference(OPL_xy, avg_ax=0)
    OPD_y = haot.optical_path_difference(OPL_xy, avg_ax=1)

    #plot_OPL_3D(x_00 * 1E2, data['Z'][0,0,:] * 1E2, OPL_xz * 1E3)
    #plot_OPL_3D(x_00 * 1E2, data['Y'][0,:,0] * 1E3, OPL_xy * 1E3)

    plot_OPD_3D(x_00 * 1E2, data['Z'][0,0,:] * 1E2, OPD_xy * 1E3)
    #plot_OPD_3D(x_00 * 1E2, data['Y'][0,:,0] * 1E3, OPD_xy * 1E3)



if __name__ == "__main__":
    data_path = ('/Users/martin/Documents/Research/UoA/Projects/LLNL/dns_analysis/plate_data/data_15/pickle')
    with open(os.path.join(data_path,'dict_3D.pickle'), "rb") as f:
        data = pickle.load(f)

    main(data)

