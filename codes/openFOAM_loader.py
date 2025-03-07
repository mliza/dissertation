import haot
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
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


# Plot OPL (wave travels on the y)
def plot_optical_path_length_x(x_range, OPL, fig_config, opl_path, time):
    plt.plot(x_range, OPL, "-", linewidth=fig_config["line_width"])
    plt.ylabel("OPL $[m]$", fontsize=fig_config["axis_label_size"])
    plt.xlabel("X $[m]$", fontsize=fig_config["axis_label_size"])
    plt.savefig(
        os.path.join(opl_path, f"opl_{time}.pdf"),
        format="pdf",
        bbox_inches="tight",
        dpi=fig_config["dpi_size"],
    )
    plt.close()


# Plot OPD (wave travels on the x)
def plot_optical_path_difference_x(x_range, OPD, fig_config, opd_path, time):
    plt.plot(x_range, OPD, "-", linewidth=fig_config["line_width"], label="Truth")
    plt.xlabel("X $[m]$", fontsize=fig_config["axis_label_size"])
    plt.ylabel("OPD $[m]$", fontsize=fig_config["axis_label_size"])
    plt.locator_params(axis="y", nbins=3)
    plt.savefig(
        os.path.join(opd_path, f"opd_{time}.pdf"),
        format="pdf",
        bbox_inches="tight",
        dpi=fig_config["dpi_size"],
    )
    plt.close()


# Plot Wavefront distortion
def plot_wavefront_distortion_x(
    x_range, y_out, wave_front_distortion, fig_config, wv_path, current_time
):
    y_loc_vec = y_out * np.ones(np.shape(x_range))
    plt.plot(
        x_range, y_loc_vec, "-", linewidth=fig_config["line_width"], label="theoretical"
    )

    plt.plot(
        x_range,
        wave_front_distortion,
        "-",
        linewidth=fig_config["line_width"],
        label="truth",
    )

    plt.legend(fontsize=fig_config["legend_size"])
    plt.yticks(
        [np.round(np.mean(wave_front_distortion), 2), y_out],
        fontsize=fig_config["ticks_size"],
    )
    plt.gca().yaxis.set_major_formatter(ScalarFormatter())
    plt.gca().ticklabel_format(useOffset=False, style="plain", axis="y")
    plt.xlabel("X $[m]$", fontsize=fig_config["axis_label_size"])
    plt.ylabel("Distortion $[m]$", fontsize=fig_config["axis_label_size"])
    plt.savefig(
        os.path.join(wd_path, f"wavefrontdistortion_{current_time}.pdf"),
        format="pdf",
        bbox_inches="tight",
        dpi=fig_config["dpi_size"],
    )
    plt.close()


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

    mesh.cell_data["permittivity_dilute"] = haot.permittivity_material(
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

    mesh.cell_data["electric"] = haot.electric_susceptibility(
        index_of_refraction["dilute"]
    )

    del index_of_refraction


def main(
    f_in,
    x_range,
    y_in,
    y_out,
    index_path,
    electric_path,
    kerl_path,
    opl_path,
    opd_path,
    wd_path,
    fig_config,
):
    # Loading foam data
    foam_case = os.path.join(f_in, "time_files")
    reader = pv.POpenFOAMReader(os.path.join(foam_case, "results.foam"))
    mesh = reader.read()
    time_data = reader.time_values
    time_data = np.array(time_data)
    plot_flag = True

    OPL = np.zeros([np.shape(time_data)[0], len(x_range)])
    y_distance = np.zeros([np.shape(time_data)[0], len(x_range)])

    # Choose the first time data for i in time_data:
    for i, current_time in enumerate(time_data):
        time = str(current_time).replace(".", "_")
        reader.set_active_time_value(current_time)
        internal_mesh = reader.read()["internalMesh"]
        cell_data = internal_mesh.cell_data
        fields_in = internal_mesh.array_names
        # Post process optics
        call_optics(internal_mesh)

        for j, current_position in enumerate(x_range):
            point_1 = [current_position, y_in, 0.0]
            point_2 = [current_position, y_out, 0.0]
            n_points = 30

            # Create a line and OPL[time, x_range]
            line_data = internal_mesh.sample_over_line(point_1, point_2, n_points)
            OPL[i][j] = haot.optical_path_length(
                line_data["index_dilute"], line_data["Distance"]
            )
        if plot_flag:
            plotter = pv.Plotter(window_size=[1800, 900])
            plotter.view_xy()
            plotter.add_mesh(
                internal_mesh,
                scalars="index_dilute",
                cmap="plasma",
                reset_camera="True",
                show_scalar_bar=False,
            )
            # clim='rng',
            plotter.set_background("white")
            plotter.camera.zoom(2.0)

            plotter.add_scalar_bar(
                title=f"Index of refraction",
                title_font_size=22,
                label_font_size=18,
                bold=True,
                position_x=0.02,
                position_y=0.6,
                width=0.3,
                n_labels=8,
                height=0.1,
                vertical=False,
                fmt="",
            )
            # Modify colorbar position and font size
            plotter.save_graphic(
                os.path.join(index_path, f"index_of_refraction_{time}.pdf")
            )
            # plotter.show()
            plotter.clear()
            plotter.close()

            # Kerl
            plotter = pv.Plotter(window_size=[1800, 900])
            plotter.view_xy()
            plotter.add_mesh(
                internal_mesh,
                scalars="kerl_polarizability",
                cmap="plasma",
                reset_camera="True",
                show_scalar_bar=False,
            )
            # clim='rng',
            plotter.set_background("white")
            plotter.camera.zoom(2.0)

            plotter.add_scalar_bar(
                title=f"Polarizability",
                title_font_size=22,
                label_font_size=18,
                bold=True,
                position_x=0.02,
                position_y=0.6,
                width=0.3,
                n_labels=8,
                height=0.1,
                vertical=False,
                fmt="",
            )
            # Modify colorbar position and font size
            plotter.save_graphic(
                os.path.join(kerl_path, f"kerl_polarizability_{time}.pdf")
            )
            plotter.clear()
            plotter.close()

            # Electric
            plotter = pv.Plotter(window_size=[1800, 900])
            plotter.view_xy()
            plotter.add_mesh(
                internal_mesh,
                scalars="electric",
                cmap="plasma",
                reset_camera="True",
                show_scalar_bar=False,
            )
            # clim='rng',
            plotter.set_background("white")
            plotter.camera.zoom(2.0)

            plotter.add_scalar_bar(
                title=f"electric susceptibility",
                title_font_size=22,
                label_font_size=18,
                bold=True,
                position_x=0.02,
                position_y=0.6,
                width=0.3,
                n_labels=8,
                height=0.1,
                vertical=False,
                fmt="",
            )
            # Modify colorbar position and font size
            plotter.save_graphic(
                os.path.join(electric_path, f"electric_susceptibility_{time}.pdf")
            )
            plotter.clear()
            plotter.close()

    # Calculate aero-optic properties
    # OPD[time,x_position] beam travels on y-axis
    OPD = haot.optical_path_difference(OPL, avg_ax=1)  # avg over space
    OPD_rms = haot.optical_path_difference_rms(OPD, avg_ax=0)
    phase_variance = haot.phase_variance(OPD_rms, 633)
    strehl_ratio = haot.strehl_ratio(phase_variance)
    y_out_vec = y_out * np.ones(np.shape(x_range))
    wave_front_distortion = y_out_vec + OPD
    print(f"The Strehl ratio is: {strehl_ratio}")

    for i, current_time in enumerate(time_data):
        time = str(current_time).replace(".", "_")
        plot_wavefront_distortion_x(
            x_range,
            y_out,
            wave_front_distortion[i],
            fig_config,
            fig_config["wd_path"],
            time,
        )

        plot_optical_path_length_x(
            x_range, OPL[i], fig_config, fig_config["opl_path"], time
        )

        plot_optical_path_difference_x(
            x_range, OPD[i], fig_config, fig_config["opd_path"], time
        )

    # TODO: move me


if __name__ == "__main__":

    f_in = "/Users/martin/Documents/Schools/UoA/Dissertation/resultsCFD/LES/openFoam"
    figures_path = os.path.join("figures", "openFoam")
    index_path = os.path.join(figures_path, "index")
    electric_path = os.path.join(figures_path, "electric")
    kerl_path = os.path.join(figures_path, "kerl")
    opl_path = os.path.join(figures_path, "opl")
    opd_path = os.path.join(figures_path, "opd")
    wd_path = os.path.join(figures_path, "wd")
    x_range = np.arange(0.3, 0.9, 0.01)
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
    fig_config["wd_path"] = wd_path
    fig_config["opd_path"] = opd_path
    fig_config["opl_path"] = opl_path

    main(
        f_in,
        x_range,
        y_in,
        y_out,
        index_path,
        electric_path,
        kerl_path,
        opl_path,
        opd_path,
        wd_path,
        fig_config,
    )
