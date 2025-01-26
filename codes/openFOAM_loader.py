import pyvista as pv
import os
import IPython
import numpy as np
import haot
import scipy.constants as s_const

# Loading foam data
foam_case = os.path.join('openFoam', 'time_files')
reader = pv.POpenFOAMReader(os.path.join(foam_case, 'results.foam'))
mesh = reader.read()
time_data = reader.time_values 
time_data = np.array(time_data)
plot_flag = False

# Choose the first time data for i in time_data:
i = 0
reader.set_active_time_value(time_data[i])
internal_mesh = mesh['internalMesh']
cell_data = internal_mesh.cell_data
fields_in = internal_mesh.array_names
point_data = internal_mesh.point_data

# Calculate optical properties
index_of_refraction = haot.index_of_refraction_density_temperature(
                                            internal_mesh['T'],
                                            internal_mesh['rho'], 'Air', 633)
kerl_polarizability = haot.kerl_polarizability_temperature(
                                            internal_mesh['T'],
                                            'Air', 633)
dielectric_constant_dilute = haot.dielectric_material_const(index_of_refraction['dilute'])
dielectric_constant_dense = haot.dielectric_material_const(index_of_refraction['dense'])

# Calculate the [x,y,z] coordinate of each cell
cell_centroids = internal_mesh.cell_centers()
x_coords = cell_centroids.points[:, 0]
y_coords = cell_centroids.points[:, 1]
z_coords = cell_centroids.points[:, 2]
n = index_of_refraction['dilute']

internal_mesh.cell_data['n'] = (index_of_refraction['dilute'] - 1) * 1E3
internal_mesh.cell_data['pol'] = kerl_polarizability * 1E30
internal_mesh.cell_data['dielectric_dilute'] = dielectric_constant_dilute * 1E12
internal_mesh.cell_data['dielectric_dense'] = dielectric_constant_dense * 1E12
internal_mesh.cell_data['index_dilute'] = index_of_refraction['dilute']

point_1 = [-0.2, 0.0, 0.0]
point_2 = [0.0, 0.0, 0.0]
n_points = 500
line_data = internal_mesh.sample_over_line(point_1, point_2, n_points)
line_coords = line_data.points
OPL = haot.optical_path_length(line_data['index_dilute'],
line_data['Distance'])
IPython.embed(colors = 'Linux')
plt.plot(line_data['Distance'], line_data['index_dilute'])





if plot_flag:
    plotter = pv.Plotter(window_size=[1800, 900])
    plotter.view_xy()
    plotter.add_mesh(internal_mesh, scalars='n', cmap='plasma',
                     reset_camera='True', show_scalar_bar=False)
                     #clim='rng', 
    plotter.set_background('white')
    plotter.camera.zoom(2.0)

    plotter.add_scalar_bar(
        title=f'(n - 1) * 1E3 at {time_data[i]} [s]',
        title_font_size=22,
        label_font_size=18,
        bold=True,
        position_x=0.02,
        position_y=0.6,
        width=0.3,
        n_labels=8,
        height=0.1,
        vertical=False
    )
# Modify colorbar position and font size
    plotter.save_graphic('index_of_refraction.pdf')
#plotter.show()
    plotter.clear()


#IPython.embed(colors = 'Linux')

# Kerl 
    plotter = pv.Plotter(window_size=[1800, 900])
    plotter.view_xy()
    plotter.add_mesh(internal_mesh, scalars='pol', cmap='plasma',
                     reset_camera='True', show_scalar_bar=False)
                     #clim='rng', 
    plotter.set_background('white')
    plotter.camera.zoom(2.0)

    plotter.add_scalar_bar(
        title=f'Polarizability * 1E-30 [kg/m3] at {time_data[i]}',
        title_font_size=22,
        label_font_size=18,
        bold=True,
        position_x=0.02,
        position_y=0.6,
        width=0.3,
        n_labels=8,
        height=0.1,
        vertical=False
    )
# Modify colorbar position and font size
    plotter.save_graphic('kerl_polarizability.pdf')
    plotter.clear()

    plotter = pv.Plotter(window_size=[1800, 900])
    plotter.view_xy()
    plotter.add_mesh(internal_mesh, scalars='dielectric_dilute', cmap='plasma',
                     reset_camera='True', show_scalar_bar=False)
                     #clim='rng', 
    plotter.set_background('white')
    plotter.camera.zoom(2.0)

    plotter.add_scalar_bar(
        title=f'Dielectric * 1E-12 [F/m] at {time_data[i]} [s]',
        title_font_size=22,
        label_font_size=18,
        bold=True,
        position_x=0.02,
        position_y=0.6,
        width=0.3,
        n_labels=8,
        height=0.1,
        vertical=False
    )
# Modify colorbar position and font size
    plotter.save_graphic('dielectric.pdf')
    plotter.clear()


