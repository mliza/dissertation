import pyvista as pv
import haot
import os 
import sys
import IPython
import numpy as np

# SU2 [N, O, NO, N2, O2]
def load_files(files_in_path):
    dict_out = { }
    for i in os.listdir(files_in_path):
        reader = pv.get_reader(os.path.join(files_in_path, i, 'flow.vtu'))
        dict_out[i] = reader.read()
    return dict_out

def plot_countour_scalar(mesh_data, scalar_field, out_path, case_name):
    plotter = call_plotter(mesh_data)
    plotter.add_mesh(mesh_data, scalars=scalar_field,
                 #cmap="coolwarm_r",
                 cmap='Spectral',
                 clim=[np.min(mesh_data[scalar_field]), 
                       np.max(mesh_data[scalar_field])],
                 show_scalar_bar=False)

    plotter.add_scalar_bar(
        title=f"{scalar_field}",
        title_font_size=22,
        label_font_size=18,
        bold=True,
        position_x=0.027,
        position_y=0.6,
        width=0.3,
        n_labels=5,
        height=0.1,
        vertical=False,
    )
    # Save the plot as an image
    output_file = os.path.join(out_path, f"{scalar_field}_{case_name}.png")
    plotter.screenshot(output_file)
    plotter.close()
    del plotter

def create_mass_density(mesh_in, species):
    mass_density = { }
    for s, val in enumerate(species):
        mass_density[val] = mesh_in.point_data_to_cell_data()[f'Density_{s}']

    return mass_density

def call_plotter(mesh):
    # Plotting setup
    plotter = pv.Plotter(off_screen=True, window_size=[1400, 800])
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
    plotter.camera.zoom(80.0)

    return plotter


def calculate_aero_props(mass_density_dict):
    index = haot.index_of_refraction(mass_density_dict)
    gladstone = haot.gladstone_dale_constant(mass_density_dict)
    dielectric = haot.dielectric_material_const(index['dilute'])
    return index, gladstone, dielectric


def main(mesh_data, fig_config):
    species = ["N", "O", "NO", "N2", "O2"]
    scalar_field = ["Temperature_ve", "Temperature_tr", "Pressure", 
                    "dilute_index", "dense_index", "gladstone_dale",
                    "dielectric"]
    out_path = 'outTest'

    for i in mesh_data:
        mass_density_dict = create_mass_density(mesh_data[i], species)
        index, gladstone, dielectric = calculate_aero_props(mass_density_dict)
        mesh_data[i]['dilute_index'] = index['dilute']
        mesh_data[i]['dense_index'] = index['dense']
        mesh_data[i]['gladstone_dale'] = gladstone['gladstone_dale']
        mesh_data[i]['dielectric'] = dielectric

        for k in scalar_field:
            plot_countour_scalar(mesh_data[i], k, out_path, i)




if __name__ == "__main__":
    abs_path = (
    "/Users/martin/Documents/Schools/UoA/Dissertation/resultsCFD/chemistryReaction"
    )
    files_in = os.path.join(abs_path, 'R_files')


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


    mesh_data = load_files(files_in)
    main(mesh_data, fig_config)

