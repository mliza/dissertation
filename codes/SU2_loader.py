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

## Users inputs ##
f_in = '/Users/martin/Documents/Schools/UoA/Dissertation/resultsCFD/LES/LES_SU2/flow'
index_path = 'index'
kerl_path = 'kerl'
plot_flag = False
index_figure = True
kerl_figure = True
y_range = np.arange(-0.7, -0.2, 0.1)
x_range = np.arange(-6, 3, 0.1)
## Users inputs ##

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
        point_1 = [4, value, 0.0]
        point_2 = [-2, value, 0.0]
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

# Calculate OPD
OPD = haot.optical_path_difference(OPL, sum_ax=0)
IPython.embed(colors = 'Linux')




"""
    #plt.plot(line_data['Distance'][:-1], OPL, label=f'{i}')
plt.plot(OPL_time[i,:] - OPL_mean, y_range, 'o-', label=f'{i}')
plt.ylabel("Distance $[m]$")
plt.xlabel("OPL $[ ]$")
plt.savefig(os.path.join("opl", f"opl_{time}.pdf"), 
            format='pdf', bbox_inches="tight")
plt.close()
"""




