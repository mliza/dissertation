import haot
import matplotlib.pyplot as plt
import numpy as np
import os
import pyvista as pv
import IPython

def call_plotter(mesh):
    # Plotting setup
    plotter = pv.Plotter(off_screen=True, window_size=[1800, 900])
    plotter.set_background("white")
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

def main(
        f_in,
        x_range,
        y_in,
        y_out,
        index_path,
        kerl_path,
        opl_path,
        opd_path,
        wd_path,
        fig_config,
        ):
    # Loading foam data
    foam_case = os.path.join(f_in, 'time_files')
    reader = pv.POpenFOAMReader(os.path.join(foam_case, 'results.foam'))
    mesh = reader.read()
    time_data = reader.time_values 
    time_data = np.array(time_data)
    plot_flag = False

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
            n_points = 500

            # Create a line and OPL[time, x_range]
            line_data = internal_mesh.sample_over_line(point_1, point_2, n_points)
            OPL[i][j] = haot.optical_path_length(line_data["index_dilute"],
                                                    line_data["Distance"])

# Calculate aero-optic properties
# TODO: NOT CHANGING OPL[:,1] 
    OPD = haot.optical_path_difference(OPL, avg_ax=1)
    OPD_rms = haot.optical_path_difference_rms(OPD, avg_ax=1)
    phase_variance = haot.phase_variance(OPD_rms, 633)
    strehl_ratio = haot.strehl_ratio(phase_variance)
    y_out_vec = y_out * np.ones(np.shape(x_range))
    wave_front_distortion = y_out_vec + OPD
    print(f'The Strehl ratio is: {strehl_ratio}')
    IPython.embed(colors = 'Linux')





    #TODO: Move Me
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

if __name__ == "__main__":

    f_in = ("/Users/martin/Documents/Schools/UoA/Dissertation/resultsCFD/LES/openFoam")
    figures_path = os.path.join("figures", "openFoam")
    index_path = os.path.join(figures_path, "index")
    kerl_path = os.path.join(figures_path, "kerl")
    opl_path = os.path.join(figures_path, "opl")
    opd_path = os.path.join(figures_path, "opd")
    wd_path = os.path.join(figures_path, "wd")
    x_range = np.arange(0.3, 0.9, 0.05)
    y_in = 0.0 
    y_out = 0.14

    # Users inputs #
    fig_config = {}
    fig_config["line_width"] = 3
    fig_config["fig_width"] = 6
    fig_config["fig_height"] = 5
    fig_config["dpi_size"] = 600
    fig_config["axis_label_size"] = 14
    fig_config["legend_size"] = 12
    fig_config["ticks_size"] = 13
    fig_config["title_size"] = 18

    main(
        f_in,
        x_range,
        y_in,
        y_out,
        index_path,
        kerl_path,
        opl_path,
        opd_path,
        wd_path,
        fig_config,
    )


