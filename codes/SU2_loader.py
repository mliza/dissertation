import haot
import matplotlib.pyplot as plt
import numpy as np
import os
import pyvista as pv
import IPython

def call_plotter(mesh):
    # Plotting setup
    plotter = pv.Plotter(off_screen=True, window_size=[1800, 900])
    plotter.set_background('white')
    plotter.view_xy()

    center = mesh.center  # [x_center, y_center, z_center]
    bounds = mesh.bounds  # [xmin, xmax, ymin, ymax, zmin, zmax]

    # Adjust the camera focal point and position to recenter
    # Shift focal point slightly
    plotter.camera.focal_point = (center[0], center[1], center[2])

    # Adjust camera height along Z-axis
    plotter.camera.position = (center[0], center[1], bounds[5] + 10)

    # Zoom
    plotter.camera.zoom(1.0)

    return plotter

def call_optics(mesh):
    cell_data = mesh.point_data_to_cell_data()

    index_of_refraction = haot.index_of_refraction_density_temperature(
                                                cell_data['Temperature'],
                                                cell_data['Density'], 'Air', 633)

    mesh.cell_data['index_dilute'] = index_of_refraction['dilute']

    mesh.cell_data['kerl_polarizability'] = haot.kerl_polarizability_temperature(
                                                cell_data['Temperature'],
                                                'Air', 633)

    mesh.cell_data['dielectric_dilute'] = haot.dielectric_material_const(
                                            index_of_refraction['dilute'])

    mesh.cell_data['critical_angle'] = haot.total_internal_reflection_angle(
                                            index_of_refraction['dilute'])

    mesh.cell_data['reflectance'] = haot.normal_incidence_reflectance(
                                            index_of_refraction['dilute'])

    mesh.cell_data['brewster_angle'] = haot.brewster_angle(
                                            index_of_refraction['dilute'])
    del index_of_refraction

def plot_index(mesh, index_path):
    mesh.cell_data['plotting_index'] = (mesh.cell_data['index_dilute'] - 1) * 1E3
    # Created helper function
    plotter = call_plotter(mesh)

    # Add mesh to the plotter with colormap
    plotter.add_mesh(
        mesh, 
        scalars='plotting_index',
        cmap='plasma', 
        show_scalar_bar=False
    )

    plotter.add_scalar_bar(
        title=f'(n - 1) * 1E3',
        title_font_size=22,
        label_font_size=18,
        bold=True,
        position_x=0.025,
        position_y=0.6,
        width=0.3,
        n_labels=8,
        height=0.1,
        vertical=False
    )

    # Save the plot as an image
    output_file = os.path.join(index_path, f"index_of_refraction_{time}.png")
    plotter.screenshot(output_file)
    plotter.close()
    del plotter

def plot_kerl(mesh, kerl_path):
    mesh.cell_data['plotting_kerl'] = mesh.cell_data['kerl_polarizability'] * 1E30
    # Created helper function
    plotter = call_plotter(mesh)

    # Add mesh to the plotter with colormap
    plotter.add_mesh(
        mesh, 
        scalars='plotting_kerl',
        cmap='plasma', 
        show_scalar_bar=False
    )

    plotter.add_scalar_bar(
        title=f'Polarizability * 1E-30',
        title_font_size=22,
        label_font_size=18,
        bold=True,
        position_x=0.025,
        position_y=0.6,
        width=0.3,
        n_labels=8,
        height=0.1,
        vertical=False
    )

    # Save the plot as an image
    output_file = os.path.join(kerl_path, f"kerl_polarizabilty_{time}.png")
    plotter.screenshot(output_file)
    plotter.close()
    del plotter

# Wave travels on the x
def plot_wavefront_distortion_y(y_range, x_loc,
                            wave_front_distortion,
                            fig_config, wd_path, time):
    x_loc_vec = x_loc * np.ones(np.shape(y_range))
    #plt.plot(x_in_vec, y_range, '-', label='In') 

    # Plot WaveFront distortion
    plt.plot(x_loc_vec, y_range, '-',
             linewidth=fig_config['line_width'],
             label='Theoretical') 
    plt.plot(wave_front_distortion, y_range, '-', 
             linewidth=fig_config['line_width'],
             label='Truth')
    plt.legend(fontsize=fig_config['legend_size'])
    plt.xticks([round(np.mean(wave_front_distortion), 3), round(x_out, 1)],      
               fontsize=fig_config['ticks_size'])
    plt.ylabel("Y $[m]$",
                fontsize=fig_config['axis_label_size'])
    plt.xlabel("Aberration $[m]$",
                fontsize=fig_config['axis_label_size'])
    plt.savefig(os.path.join(wd_path, f"wavefrontDistortion_{time}.pdf"), 
                format='pdf', bbox_inches="tight",
                dpi=fig_config['dpi_size'])
    plt.close()

# Plot OPL (wave travels on the x)
def plot_optical_path_length_y(y_range, OPL,
                               fig_config, opl_path, time):
    plt.plot(OPL, y_range, '-', 
             linewidth=fig_config['line_width'])
    plt.ylabel("y-distance $[m]$",
                fontsize=fig_config['axis_label_size'])
    plt.xlabel("OPL $[m]$",
                fontsize=fig_config['axis_label_size'])
    plt.savefig(os.path.join(opl_path, f"opl_{time}.pdf"), 
                format='pdf', bbox_inches="tight",
                dpi=fig_config['dpi_size'])
    plt.close()

# Plot OPD (wave travels on the x)
def plot_optical_path_difference_y(y_range, OPD,
                               fig_config, opd_path, time):
    plot_optical_path_difference_y
    plt.plot(OPD, y_range, '-', 
             linewidth=fig_config['line_width'],
             label='Truth')
    plt.ylabel("y-distance $[m]$",
                fontsize=fig_config['axis_label_size'])
    plt.xlabel("OPD $[m]$",
                fontsize=fig_config['axis_label_size'])
    plt.locator_params(axis='x', nbins=3)
    plt.savefig(os.path.join(opd_path, f"opd_{time}.pdf"), 
                format='pdf', bbox_inches="tight",
                dpi=fig_config['dpi_size'])
    plt.close()


## Users inputs ##
f_in = '/Users/martin/Documents/Schools/UoA/Dissertation/resultsCFD/LES/LES_SU2/flow'
index_path = 'figures/index'
kerl_path = 'figures/kerl'
opl_path = 'figures/opl'
opd_path = 'figures/opd'
wd_path = 'figures/wd'
plot_flag = True 
index_figure = True
kerl_figure = True
y_range = np.arange(-0.7, -0.2, 0.01)
x_range = np.arange(-6, 3, 0.1)
# Where beam goes in
x_in = 4
x_out = -3
## Users inputs ##
fig_config = {}
fig_config["line_width"] = 3
fig_config["fig_width"] = 6
fig_config["fig_height"] = 5
fig_config["dpi_size"] = 600
fig_config["axis_label_size"] = 14
fig_config["legend_size"] = 12
fig_config["ticks_size"] = 13
fig_config["title_size"] = 18

# Testing flag
test_flag = False

# Looking for surface and flow files
vtu_f = [x for x in os.listdir(f_in) if x.split('.')[1] == 'vtu']
surface_files = [x for x in sorted(vtu_f) if x.split('_')[0] == 'surface']
flow_files = [x for x in sorted(vtu_f) if x.split('_')[0] == 'flow']

if test_flag:
    flow_files = flow_files[:1]
    plot_flag = False

# OPL[time, y_range], sum on x_range
OPL = np.zeros([np.shape(flow_files)[0], len(y_range)])

# Make this a for loop base in time steps
for i, val in enumerate(flow_files):
    time = val.split('.')[0].split('_')[-1]
    reader = pv.get_reader(os.path.join(f_in, val))
    mesh = reader.read()

    # Calculate optical properties and populate the mesh object
    call_optics(mesh)

    for j, value in enumerate(y_range):
        # Get line data [x, y, z]
        point_1 = [x_in, value, 0.0]
        point_2 = [x_out, value, 0.0]
        n_points = 900

        # Create a line and OPL[time, y_range]
        line_data = mesh.sample_over_line(point_1, point_2, n_points)
        OPL_vect = haot.optical_path_length(line_data['index_dilute'],
                                       line_data['Distance'])

        # Create OPL [time, y_range] sum on x_range
        OPL[i][j] = np.sum(OPL_vect)

        # Free resources
        del line_data
        del OPL_vect

    if plot_flag:
        if index_figure:
            plot_index(mesh, index_path)

        if kerl_figure:
            plot_kerl(mesh, kerl_path)

    # Clean resources
    del reader
    del mesh

# Calculate OPD and WaveFront distortion
OPD = haot.optical_path_difference(OPL, sum_ax=0)
x_in_vec = x_in * np.ones(np.shape(y_range))
x_out_vec = x_out * np.ones(np.shape(y_range))
wave_front_distortion = x_out_vec + OPD

for i, val in enumerate(flow_files):
    time = val.split('.')[0].split('_')[-1]

    # Plot wavefront distortion (wave travels on x)
    plot_wavefront_distortion_y(y_range, x_out,
                                wave_front_distortion[i,:],
                                fig_config, wd_path, time)

    # Plot OPL (wave travels on x)
    plot_optical_path_length_y(y_range, OPL[i,:],
                                fig_config, opl_path, time)

    # Plot OPD (wave travels on x)
    plot_optical_path_difference_y(y_range, OPD[i,:],
                                fig_config, opd_path, time)
