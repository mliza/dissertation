import numpy as np
import haot
import pyvista as pv
import IPython
import os
import matplotlib.pyplot as plt

def call_plotter(mesh):
    # Plotting setup
    plotter = pv.Plotter(off_screen=True, window_size=[1800, 900])
    plotter.set_background('white')
    plotter.view_xy()

    center = mesh.center  # [x_center, y_center, z_center]
    bounds = mesh.bounds  # [xmin, xmax, ymin, ymax, zmin, zmax]

    # Adjust the camera focal point and position to recenter
    plotter.camera.focal_point = (center[0], center[1], center[2])  # Shift focal point slightly
    plotter.camera.position = (center[0], center[1], bounds[5] + 10)  # Adjust camera height along Z-axis

    plotter.camera.zoom(1.0)

    return plotter


## Users inputs ##
f_in = 'LES_SU2/flow' 
index_path = 'index'
kerl_path = 'kerl'
plot_flag = True 
index_figure = True 
kerl_figure = True
y_range = np.arange(-0.7, -0.2, 0.1)
x_range = np.arange(-6, 3, 0.1)
## Users inputs ##
# TODO
OPL_mean = [ 3003.17522628, 3003.1752767, 3003.17522919, 3003.1751412,
            3003.17484716]

# Testing flag 
test_flag = False 

# Looking for surface and flow files
vtu_f = [x for x in os.listdir(f_in) if x.split('.')[1] == 'vtu']
surface_files = [x for x in sorted(vtu_f) if x.split('_')[0] == 'surface']
flow_files = [x for x in sorted(vtu_f) if x.split('_')[0] == 'flow']
if test_flag:
    flow_files = flow_files[:1] 
    plot_flag = False 

OPL_time = np.zeros([np.shape(flow_files)[0], len(y_range)])

# Make this a for loop base in time steps
for i, val in enumerate(flow_files):
    time = val.split('.')[0].split('_')[-1]
    reader = pv.get_reader(os.path.join(f_in, val))
    mesh = reader.read()
    cell_data = mesh.point_data_to_cell_data()
    fields_in = mesh.array_names
    centroids = mesh.cell_centers()
    centroid_coords = centroids.points #[X, Y, Z]

    # Remove last column of zeros
    axis_xy = np.delete(centroid_coords, np.s_[-1:], axis=1)


    # Calculate Contour optical properties
    index_of_refraction = haot.index_of_refraction_density_temperature(
                                                cell_data['Temperature'],
                                                cell_data['Density'], 'Air', 633)
    kerl_polarizability = haot.kerl_polarizability_temperature(
                                                cell_data['Temperature'],
                                                'Air', 633)
    dielectric_constant = haot.dielectric_material_const(index_of_refraction['dilute'])
    critical_angle = haot.total_internal_reflection_angle(index_of_refraction['dilute'])
    reflectance = haot.normal_incidence_reflectance(index_of_refraction['dilute'])

    mesh.cell_data['index_dilute'] = (index_of_refraction['dilute'] - 1)* 1E3 
    mesh.cell_data['kerl_polarizability'] = kerl_polarizability * 1E30
    mesh.cell_data['index_dilute'] = index_of_refraction['dilute']

    for j, value in enumerate(y_range):
        # Get line data [x, y, z]
        point_1 = [4, value, 0.0]
        point_2 = [-2, value, 0.0]
        n_points = 1000

        # Create a line
        line_data = mesh.sample_over_line(point_1, point_2, n_points)
        line_coords = line_data.points
        OPL = haot.optical_path_length(line_data['index_dilute'],
                                       line_data['Distance'])

        # Create OPL as a function of time
        OPL_time[i][j] = np.sum(OPL)

        if test_flag:
            IPython.embed(colors = 'Linux')

        #plt.plot(line_data['Distance'][:-1], OPL, label=f'{i}')
    plt.plot(OPL_time[i,:] - OPL_mean, y_range, 'o-', label=f'{i}')
    plt.ylabel("Distance $[m]$")
    plt.xlabel("OPL $[ ]$")
    plt.savefig(os.path.join("opl", f"opl_{time}.pdf"), 
                format='pdf', bbox_inches="tight")
    plt.close()

    if plot_flag:
        # Add index of refraction data to the mesh
        mesh.cell_data['Index_of_Refraction'] = (index_of_refraction['dilute'] - 1)* 1E3 
        mesh.cell_data['kerl_polarizability'] = kerl_polarizability * 1E30

        if index_figure:
            # Created helper function
            plotter = call_plotter(mesh)

            # Add mesh to the plotter with colormap
            plotter.add_mesh(
                mesh, 
                scalars='index_dilute', 
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


        if kerl_figure: 
            # Created helper function
            plotter = call_plotter(mesh)

            # Add mesh to the plotter with colormap
            plotter.add_mesh(
                mesh, 
                scalars='kerl_polarizability', 
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

        # Clean resources
        del reader
        del mesh
        del plotter
        del cell_data
        del centroids
        del index_of_refraction
        del kerl_polarizability
        del dielectric_constant
        del critical_angle
        del reflectance


OPL_mean = np.mean(OPL_time, axis=0)




