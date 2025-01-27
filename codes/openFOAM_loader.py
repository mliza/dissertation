import haot
import matplotlib.pyplot as plt
import numpy as np
import os
import pyvista as pv
import IPython

# Process optical properties
def call_optics(mesh):
    cell_data = mesh.point_data_to_cell_data()

    index_of_refraction = haot.index_of_refraction_density_temperature(
        cell_data["T"], cell_data["rho"], "Air", 633
    )

    mesh.cell_data["index_dilute"] = index_of_refraction["dilute"]

    mesh.cell_data["kerl_polarizability"] = haot.kerl_polarizability_temperature(
        cell_data["T"], "Air", 633
    )

    mesh.cell_data["dielectric_dilute"] = haot.dielectric_material_const(
        index_of_refraction["dilute"]
    )

    mesh.cell_data["critical_angle"] = haot.total_internal_reflection_angle(
        index_of_refraction["dilute"]
    )

    mesh.cell_data["reflectance"] = haot.normal_incidence_reflectance(
        index_of_refraction["dilute"]
    )

    mesh.cell_data["brewster_angle"] = haot.brewster_angle(
        index_of_refraction["dilute"]
    )
    del index_of_refraction

# Loading foam data
f_in =(
"/Users/martin/Documents/Schools/UoA/Dissertation/resultsCFD/LES/openFoam")
foam_case = os.path.join(f_in, 'time_files')
reader = pv.POpenFOAMReader(os.path.join(foam_case, 'results.foam'))
mesh = reader.read()
time_data = reader.time_values 
time_data = np.array(time_data)
x_range = (1.1, 1.6, 0.01)
plot_flag = False
y_in = -0.1 
y_out = 0.15

OPL = np.zeros([np.shape(time_data)[0], len(x_range)])

# Choose the first time data for i in time_data:
for i, val in enumerate(time_data):
    reader.set_active_time_value(time_data[i])
    internal_mesh = mesh['internalMesh']
    cell_data = internal_mesh.cell_data
    fields_in = internal_mesh.array_names
# Post process optics
    call_optics(internal_mesh)

    for j, value in enumerate(x_range): 
        point_1 = [value, y_in, 0.0]
        point_2 = [value, y_out, 0.0]
        n_points = 900

        # Create a line and OPL[time, x_range]
        line_data = internal_mesh.sample_over_line(point_1, point_2, n_points)
        OPL_vect = haot.optical_path_length(line_data["index_dilute"],
                                                line_data["Distance"])

        OPL[i][j] = np.sum(OPL_vect)

OPD = haot.optical_path_difference(OPL, sum_ax=0)
y_out_vec = y_out * np.ones(np.shape(x_range))
wave_front_distortion = y_out_vec + OPD


IPython.embed(colors = 'Linux')



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


