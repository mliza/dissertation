import pyvista as pv
import haot
import os 
import sys
import IPython
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


# SU2 [N, O, NO, N2, O2]
def load_files(files_in_path):
    dict_out = { }
    for i in os.listdir(files_in_path):
        reader = pv.get_reader(os.path.join(files_in_path, i, 'flow.vtu'))
        dict_out[i] = reader.read()
    return dict_out

def plot_countour_scalar(mesh_data, case_name, scalar_field, fig_config):
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
    output_file = os.path.join(fig_config["out_path"], f"{case_name}_{scalar_field}.png")
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

def plot_stagnation_data(line_data, fig_config):
    noneq = sorted([x for x in line_data.keys() if x.split("_")[1] ==
                    "nonequilibrium"])
    frozen = sorted([x for x in line_data.keys() if x.split("_")[1] ==
                     "frozen"])
    cases = ['1R', '2R', '3R']
    neutral = ["N", "O", "NO", "N2", "O2"]

    colors = [
        mcolors.TABLEAU_COLORS["tab:blue"],
        mcolors.TABLEAU_COLORS["tab:orange"],
        mcolors.TABLEAU_COLORS["tab:green"],
        mcolors.TABLEAU_COLORS["tab:red"],
        mcolors.TABLEAU_COLORS["tab:purple"],
    ]

    for i in cases:
        # First nonzero index
        noneq = f"{i}_nonequilibrium"
        frozen = f"{i}_frozen"

        cut_indx = np.argmax(np.diff(line_data[frozen]['Temperature_ve']) != 0) 
        # Get Distances
        noneq_mm = (line_data[noneq]['Distance'][cut_indx:] -
                    np.max(line_data[noneq]['Distance'][cut_indx:])) * 1e3
        frozen_mm = (line_data[frozen]['Distance'][cut_indx:] -
                    np.max(line_data[frozen]['Distance'][cut_indx:])) * 1e3

        ## Plot Temperatures ##
        plt.plot(noneq_mm, line_data[noneq]['Temperature_tr'][cut_indx:], 
                 color=colors[0],
                 linewidth=fig_config["line_width"],
                 label="$T_{tr}$")
                 
        plt.plot(noneq_mm, line_data[noneq]['Temperature_ve'][cut_indx:], 
                 color=colors[1],
                 linewidth=fig_config["line_width"],
                 label="$T_{vib}$")

        plt.plot(frozen_mm, line_data[frozen]['Temperature_tr'][cut_indx:], 
                 "-.",
                 color=colors[0],
                 linewidth=fig_config["line_width"])
                 
        plt.plot(frozen_mm, line_data[frozen]['Temperature_ve'][cut_indx:], 
                 "-.",
                 color=colors[1],
                 linewidth=fig_config["line_width"])
        
        plt.xlabel("X $[mm]$", fontsize=fig_config["axis_label_size"])
        plt.ylabel("T $[K]$", fontsize=fig_config["axis_label_size"])

        plt.xticks(fontsize=fig_config["ticks_size"])
        plt.yticks(fontsize=fig_config["ticks_size"])
        plt.legend(fontsize=fig_config['legend_size'])

        plt.savefig(
            os.path.join(fig_config["out_path"], f"{i}_temperatures.pdf"),
            format="pdf",
            bbox_inches="tight",
            dpi=fig_config["dpi_size"],
        )
        plt.close()
        ## Plot Temperatures ##

        ## Plot Pressure ##
        plt.plot(noneq_mm, line_data[noneq]['Pressure'][cut_indx:] * 1e-3, 
                 color=colors[0],
                 linewidth=fig_config["line_width"],
                 label="Nonequilibrium")

        plt.plot(frozen_mm, line_data[frozen]['Pressure'][cut_indx:] * 1e-3, 
                 color=colors[1],
                 linewidth=fig_config["line_width"],
                 label="Frozen")
        
        plt.xlabel("X $[mm]$", fontsize=fig_config["axis_label_size"])
        plt.ylabel("P $[kPa]$", fontsize=fig_config["axis_label_size"])

        plt.xticks(fontsize=fig_config["ticks_size"])
        plt.yticks(fontsize=fig_config["ticks_size"])
        plt.legend(fontsize=fig_config["legend_size"])

        plt.savefig(
            os.path.join(fig_config["out_path"], f"{i}_pressures.pdf"),
            format="pdf",
            bbox_inches="tight",
            dpi=fig_config["dpi_size"],
        )
        plt.close()
        ## Plot Pressure ##

        ## Plot Mass Fraction ##
        for s, value in enumerate(neutral):
            plt.plot(
                noneq_mm,
                line_data[noneq][f"MassFrac_{s}"][cut_indx:],
                color=colors[s],
                linewidth=fig_config["line_width"],
                label=value,
            )

            plt.plot(
                frozen_mm,
                line_data[frozen][f"MassFrac_{s}"][cut_indx:],
                "-.",
                color=colors[s],
                linewidth=fig_config["line_width"],
            )
    
        plt.xlabel("X $[mm]$", fontsize=fig_config["axis_label_size"])
        plt.ylabel("Mass Fraction $[ ]$", fontsize=fig_config["axis_label_size"])

        plt.xticks(fontsize=fig_config["ticks_size"])
        plt.yticks(fontsize=fig_config["ticks_size"])
        plt.legend(fontsize=fig_config["legend_size"])

        plt.savefig(
            os.path.join(fig_config["out_path"], f"{i}_massFraction.pdf"),
            format="pdf",
            bbox_inches="tight",
            dpi=fig_config["dpi_size"],
        )
        plt.close()
        ## Plot Mass Fraction ##


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
    
    point_1 = [-0.01, 0.0, 0.0]
    point_2 = [0.0, 0.0, 0.0]
    n_points = 100
   
    line_dict = { }

    for i in mesh_data:
        mass_density_dict = create_mass_density(mesh_data[i], species)
        index, gladstone, dielectric = calculate_aero_props(mass_density_dict)
        mesh_data[i]['dilute_index'] = index['dilute']
        mesh_data[i]['dense_index'] = index['dense']
        mesh_data[i]['gladstone_dale'] = gladstone['gladstone_dale']
        mesh_data[i]['dielectric'] = dielectric

        # Get Line Data
        line_dict[i] = mesh_data[i].sample_over_line(point_1, point_2, n_points)

        # Generate Plots
        for k in scalar_field:
            plot_countour_scalar(mesh_data[i], i, k, fig_config)
            
    plot_stagnation_data(line_dict, fig_config)



if __name__ == "__main__":
    abs_path = (
    "/Users/martin/Documents/Schools/UoA/Dissertation/resultsCFD/chemistryReaction"
    )
    files_in = os.path.join(abs_path, 'R_files')
    fig_out_path = 'outTest'

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
    fig_config["out_path"] = fig_out_path

    mesh_data = load_files(files_in)
    main(mesh_data, fig_config)

