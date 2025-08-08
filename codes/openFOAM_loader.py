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


def plot_scalar_contour(internal_mesh, scalar_field, title_field, path_out, time):
    # https://matplotlib.org/stable/users/explain/colors/colormaps.html
    plotter = pv.Plotter(window_size=[1800, 900])
    plotter.view_xy()
    plotter.add_mesh(
        internal_mesh,
        scalars=f"{scalar_field}",
        cmap="turbo",
        reset_camera="True",
        show_scalar_bar=False,
    )
    # clim='rng',
    plotter.set_background("white")
    plotter.camera.zoom(2.0)

    plotter.add_scalar_bar(
        title=f"{title_field}",
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
    plotter.save_graphic(os.path.join(path_out, f"{scalar_field}_{time}.pdf"))
    plotter.clear()
    plotter.close()


def plot_OPD_3D(time_data, x_range, OPD, fig_config):
    T, X = np.meshgrid(x_range, time_data)
    fig = plt.figure(figsize=(fig_config["fig_width"], fig_config["fig_height"]))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(T, X, OPD, cmap="turbo", edgecolor="none")
    ax.set_xlabel("X $[cm]$", fontsize=fig_config["axis_label_size"])
    ax.set_ylabel("Time $[s]$", fontsize=fig_config["axis_label_size"])
    ax.set_zlabel("OPD $[cm]$", labelpad=20, fontsize=fig_config["axis_label_size"])
    ax.tick_params(axis="z", pad=10)
    plt.savefig(
        os.path.join(fig_config["tmp_path"], f"OPD_3D.pdf"),
        format="pdf",
        # bbox_inches="tight",
    )
    plt.close()

    fig, ax = plt.subplots(figsize=(fig_config["fig_width"], fig_config["fig_height"]))
    contour = ax.contourf(T, X, OPD, levels=5, cmap="turbo")
    cbar = plt.colorbar(contour, ax=ax)
    ax.set_xlabel("X $[cm]$", fontsize=fig_config["axis_label_size"])
    ax.set_ylabel("Time $[s]$", fontsize=fig_config["axis_label_size"])
    plt.savefig(
        os.path.join(fig_config["tmp_path"], f"OPD_contour.pdf"),
        format="pdf",
        bbox_inches="tight",
        dpi=fig_config["dpi_size"],
    )
    plt.close()


def plot_OPL_3D(time_data, x_range, OPL, fig_config):
    T, X = np.meshgrid(x_range, time_data)
    fig = plt.figure(figsize=(fig_config["fig_width"], fig_config["fig_height"]))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(T, X, OPL, cmap="turbo", edgecolor="none")
    ax.set_xlabel("X $[cm]$", fontsize=fig_config["axis_label_size"])
    ax.set_ylabel("Time $[s]$", fontsize=fig_config["axis_label_size"])
    ax.set_zlabel("OPL $[cm]$", labelpad=20, fontsize=fig_config["axis_label_size"])
    ax.tick_params(axis="z", pad=10)
    plt.savefig(
        os.path.join(fig_config["tmp_path"], f"OPL_3D.pdf"),
        format="pdf",
        # bbox_inches="tight",
    )
    plt.close()

    fig, ax = plt.subplots(figsize=(fig_config["fig_width"], fig_config["fig_height"]))
    contour = ax.contourf(T, X, OPL, levels=5, cmap="turbo")
    cbar = plt.colorbar(contour, ax=ax)
    ax.set_xlabel("X $[cm]$", fontsize=fig_config["axis_label_size"])
    ax.set_ylabel("Time $[s]$", fontsize=fig_config["axis_label_size"])
    plt.savefig(
        os.path.join(fig_config["tmp_path"], f"OPL_contour.pdf"),
        format="pdf",
        bbox_inches="tight",
        dpi=fig_config["dpi_size"],
    )
    plt.close()


# Plot OPL (wave travels on the y)
def plot_optical_path_length_x(x_range, OPL, spatial_var, fig_config, opl_path, time):

    fig = plt.figure(figsize=(fig_config["fig_width"], fig_config["fig_height"]))
    plt.plot(x_range, OPL * 10, "-", linewidth=fig_config["line_width"],
             label=f'$\sigma_x$={spatial_var:0.3}')
    plt.ticklabel_format(style='plain', axis='y')
    plt.gca().yaxis.get_major_formatter().set_useOffset(False)
    plt.ylabel("OPL $[mm]$", fontsize=fig_config["axis_label_size"])
    plt.xlabel("X $[cm]$", fontsize=fig_config["axis_label_size"])
    plt.legend(fontsize=fig_config["legend_size"])
    plt.savefig(
        os.path.join(opl_path, f"opl_{time}.pdf"),
        format="pdf",
        bbox_inches="tight",
        dpi=fig_config["dpi_size"],
    )
    plt.close()

def plot_optical_path_length_shift(x_range, y_out, OPL, wavelength_nm, fig_config,
                                   opl_shift_path, cur_time):

    my_time = float(cur_time.replace('_', '.'))
    freq_Hz = (3 * 1E8) / (wavelength_nm * 1E-9)
    amplitude = 1
    y_range =  np.linspace(0, y_out, len(x_range))
    truth = amplitude * np.sin(2 * np.pi * freq_Hz * my_time * x_range /
                               (wavelength_nm * 1E-7))
    shift = amplitude * np.sin(2 * np.pi * freq_Hz * my_time * (x_range + OPL)
                               / (wavelength_nm * 1E-7))


    plt.scatter(x_range, y_out + OPL, linewidth=fig_config["line_width"],
    label=f'Y_out = {y_out} $[cm]$')
    plt.ylabel("OPL $[cm]$", fontsize=fig_config["axis_label_size"])
    plt.xlabel("X $[cm]$", fontsize=fig_config["axis_label_size"])
    plt.legend(fontsize=fig_config["legend_size"])

    """
    fig = plt.figure(figsize=(fig_config["fig_width"], fig_config["fig_height"]))
    plt.plot(x_range, truth, "-", linewidth=fig_config["line_width"],
    label='PPL')
    plt.plot(x_range, shift, "-", linewidth=fig_config["line_width"],
    label='OPL')
    plt.ylabel("Amplitude $[cm]$", fontsize=fig_config["axis_label_size"])
    plt.xlabel("X $[cm]$", fontsize=fig_config["axis_label_size"])
    plt.legend(fontsize=fig_config["legend_size"])
    """
    plt.savefig(
        os.path.join(opl_shift_path, f"opl_shift_{cur_time}.pdf"),
        format="pdf",
        bbox_inches="tight",
        dpi=fig_config["dpi_size"],
    )
    plt.close()


# Plot OPD (wave travels on the x)
def plot_optical_path_difference_x(x_range, OPD, opl_mean, fig_config, opd_path, time):
    fig = plt.figure(figsize=(fig_config["fig_width"], fig_config["fig_height"]))

    plt.plot(x_range, OPD * 1E7, "-", linewidth=fig_config["line_width"],
             label=fr'$\overline{{OPL_x}} = {opl_mean:0.3}$')
    plt.ylabel("OPD $[nm]$", fontsize=fig_config["axis_label_size"])
    plt.xlabel("X $[cm]$", fontsize=fig_config["axis_label_size"])
    plt.legend(fontsize=fig_config["legend_size"])
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
    fig = plt.figure(figsize=(fig_config["fig_width"], fig_config["fig_height"]))
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
        [y_out],
        fontsize=fig_config["ticks_size"],
    )
    plt.gca().yaxis.set_major_formatter(ScalarFormatter())
    plt.gca().ticklabel_format(useOffset=False, style="plain", axis="y")
    plt.xlabel("X $[cm]$", fontsize=fig_config["axis_label_size"])
    plt.ylabel("WD $[cm]$", fontsize=fig_config["axis_label_size"])
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

    mesh.cell_data["Unorm"] = np.linalg.norm(cell_data["U"], axis=1)

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

    mesh.cell_data["susceptibility_dilute"] = haot.electric_susceptibility(
        index_of_refraction["dilute"]
    )

    del index_of_refraction


def plot_time_mean(OPL, OPD, x_range, y_out_vec, fig_config):
    # OPL
    fig = plt.figure(figsize=(fig_config["fig_width"], fig_config["fig_height"]))
    plt.plot(x_range, np.mean(OPL, axis=0), "-", linewidth=fig_config["line_width"])
    plt.xlabel("X $[cm]$", fontsize=fig_config["axis_label_size"])
    plt.ylabel("$\\overline{OPL} [cm]$", fontsize=fig_config["axis_label_size"])
    plt.locator_params(axis="y", nbins=4)
    plt.savefig(
        os.path.join(fig_config["tmp_path"], f"OPL_mean.pdf"),
        format="pdf",
        bbox_inches="tight",
        dpi=fig_config["dpi_size"],
    )
    plt.close()

    # OPD
    fig = plt.figure(figsize=(fig_config["fig_width"], fig_config["fig_height"]))
    plt.plot(x_range, np.mean(OPD, axis=0), "-", linewidth=fig_config["line_width"])
    plt.xlabel("X $[cm]$", fontsize=fig_config["axis_label_size"])
    plt.ylabel("$\\overline{OPD} [cm]$", fontsize=fig_config["axis_label_size"])
    plt.locator_params(axis="y", nbins=4)
    plt.savefig(
        os.path.join(fig_config["tmp_path"], f"OPD_mean.pdf"),
        format="pdf",
        bbox_inches="tight",
        dpi=fig_config["dpi_size"],
    )
    plt.close()

    # Wave front
    fig = plt.figure(figsize=(fig_config["fig_width"], fig_config["fig_height"]))
    plt.plot(
        x_range, y_out_vec, "-", linewidth=fig_config["line_width"], label="theoretical"
    )
    plt.plot(
        x_range,
        np.mean(OPD, axis=0) + y_out_vec,
        "-",
        linewidth=fig_config["line_width"],
        label="truth",
    )

    plt.legend(fontsize=fig_config["legend_size"])
    plt.gca().yaxis.set_major_formatter(ScalarFormatter())
    plt.gca().ticklabel_format(useOffset=False, style="plain", axis="y")
    plt.xlabel("X $[cm]$", fontsize=fig_config["axis_label_size"])
    plt.ylabel("$\\overline{WD}$ $[cm]$", fontsize=fig_config["axis_label_size"])
    plt.savefig(
        os.path.join(fig_config["tmp_path"], f"WD_mean.pdf"),
        format="pdf",
        bbox_inches="tight",
        dpi=fig_config["dpi_size"],
    )
    plt.close()


def main(
    f_in,
    x_range,
    y_in,
    y_out,
    plot_fields,
    title_fields,
    path_out,
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
    plot_flag = False

    OPL = np.zeros([np.shape(time_data)[0], len(x_range)])
    y_distance = np.zeros([np.shape(time_data)[0], len(x_range)])

    # Choose the first time data for i in time_data:
    #TODO: time_data
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
            for indx, val in enumerate(plot_fields):
                plot_scalar_contour(
                    internal_mesh, val, title_fields[indx], path_out[indx], time
                )

    # Calculate aero-optic properties
    # OPD[time,x_position] beam travels on y-axis
    #TODO: DO OPD as afunction of TIME
    OPD = haot.optical_path_difference(OPL, avg_ax=1)  # avg space
    OPD_time = haot.optical_path_difference(OPL, avg_ax=0)  # avg time

    OPD_rms = haot.optical_path_difference_rms(OPD, avg_ax=0)
    phase_variance = haot.phase_variance(OPD_rms, 633)
    strehl_ratio = haot.strehl_ratio(phase_variance)
    y_out_vec = y_out * np.ones(np.shape(x_range))
    wave_front_distortion = y_out_vec + OPD
    time_var = np.mean(np.std(OPL, axis=0))
    spatial_var = np.mean(np.std(OPL, axis=1))
    mean_space_OPL = np.mean(np.mean(OPL, axis=1))
    mean_time_OPL = np.mean(np.mean(OPL, axis=0))

    print(f"The Strehl ratio is: {strehl_ratio:0.4}")
    print(f"Spatial_var: {spatial_var:0.4}")
    print(f"Time_var: {time_var:0.4}")
    print(f"OPL_mean_space: {mean_space_OPL:0.4}")
    print(f"OPL_mean_time: {mean_time_OPL:0.4}")

    # 3D plots
    plot_OPL_3D(time_data, x_range, OPL, fig_config)
    plot_OPD_3D(time_data, x_range, OPL, fig_config)
    plot_time_mean(OPL, OPD, x_range, y_out_vec, fig_config)

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
            x_range, OPL[i], spatial_var, fig_config, fig_config["opl_path"], time
        )

        plot_optical_path_length_shift(x_range, y_out, OPL[i], 633, fig_config,
                                       fig_config["opl_shift"], time)

        plot_optical_path_difference_x(
            x_range, OPD[i], mean_time_OPL, fig_config, fig_config["opd_path"], time)


if __name__ == "__main__":

    f_in = "/Users/martin/Documents/Schools/UoA/Dissertation/resultsCFD/LES/openFoam"
    figures_path = os.path.join("figures", "openFoam")
    figures_path = os.path.join("newFigures", "openFoam")
    index_path = os.path.join(figures_path, "index")
    susceptibility_path = os.path.join(figures_path, "susceptibility")
    velocity_path = os.path.join(figures_path, "velocityMag")
    permittivity_path = os.path.join(figures_path, "permittivity")
    kerl_path = os.path.join(figures_path, "kerl")
    opl_path = os.path.join(figures_path, "opl")
    opl_shift = os.path.join(figures_path, "oplShift")
    opd_path = os.path.join(figures_path, "opd")
    wd_path = os.path.join(figures_path, "wd")
    tmp_path = os.path.join(figures_path, "tmp")
    temperature_path = os.path.join(figures_path, "temperature")
    x_range = np.arange(0.3, 0.9, 0.01)
    y_in = 0.0
    y_out = 0.17

    # Users inputs #
    fig_config = {}
    fig_config["line_width"] = 3
    fig_config["fig_width"] = 8
    fig_config["fig_height"] = 6
    fig_config["dpi_size"] = 600
    fig_config["axis_label_size"] = 14
    fig_config["legend_size"] = 12
    fig_config["ticks_size"] = 13
    fig_config["title_size"] = 18
    fig_config["wd_path"] = wd_path
    fig_config["opd_path"] = opd_path
    fig_config["opl_path"] = opl_path
    fig_config["opl_shift"] = opl_shift
    fig_config["tmp_path"] = tmp_path

    # There is a maximum of two
    plot_scalars = ["kerl_polarizability", "permittivity_dilute"]
    title_fields = ["Polarizability", "Permittivity"]
    path_out = [kerl_path, permittivity_path]

    plot_scalars = ["index_dilute", "T"]
    title_fields = ["Index of refraction", "Temperature"]
    path_out = [index_path, temperature_path]

    plot_scalars = ["susceptibility_dilute", "Unorm"]
    title_fields = ["Electric susceptibility", "Velocity magnitude"]
    path_out = [susceptibility_path, velocity_path]

    main(
        f_in,
        x_range,
        y_in,
        y_out,
        plot_scalars,
        title_fields,
        path_out,
        opl_path,
        opd_path,
        wd_path,
        fig_config,
    )
