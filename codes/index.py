import haot
import matplotlib.pyplot as plt
import figure_configurations
import numpy as np
from ambiance import Atmosphere
import IPython



# User Inputs #
altitude = np.linspace(0, 81e3, 1000) #(0 to 81) [km]
mach_in = np.linspace(0.4, 25, 1000) #(0.4 to 10) [mach]
wavelength_nm = 633 

atm = Atmosphere(altitude)
normal_relations = haot.normal_shock_relations(mach_in)
density = atm.density
temperature = atm.temperature
density_2 = normal_relations['density_r'] * density
temperature_2 = normal_relations['temperature_r'] * temperature
mach_2 = normal_relations['mach_2']

index_post_shock = haot.index_of_refraction_density_temperature(temperature_2,
                                                                density_2,
                                                                "Air",
                                                                wavelength_nm)
fig_config = figure_configurations.figure_settings()
fig, ax1 = plt.subplots(figsize=(fig_config["fig_width"] + 2, fig_config["fig_height"]))
ax1.semilogy(mach_2, index_post_shock['dilute'] - 1,
             linewidth=fig_config["line_width"], label='Dilute')
ax1.semilogy(mach_2, index_post_shock['dilute'] - 1,
             linewidth=fig_config["line_width"], label='Dense')

ax1.set_xlabel('Mach $[ ]$', fontsize=fig_config["axis_label_size"])
ax1.set_ylabel('n - 1 $[ ]$', fontsize=fig_config["axis_label_size"])
ax1.legend(fontsize=fig_config["legend_size"])

ax2 = ax1.twiny()
ax2.set_xlim(ax1.get_xlim())

# Set ticks to match ax1's temperature ticks, but label with density values
temp_ticks = ax1.get_xticks()
ax2.set_xticks(temp_ticks)
ax2.set_xticklabels([f"{rho:.4f}" for rho in np.interp(temp_ticks,
                                                       altitude, density_2)])

ax2.set_xlabel(r'$\rho$ [kg/m$^3$]', fontsize=fig_config["axis_label_size"])
plt.savefig(f'dilute_dense_mach_{wavelength_nm}.pdf', format="pdf", bbox_inches="tight",
            dpi=fig_config["dpi_size"])
plt.close()


fig_config = figure_configurations.figure_settings()
fig, ax1 = plt.subplots(figsize=(fig_config["fig_width"] + 2, fig_config["fig_height"]))
ax1.semilogy(altitude, index_post_shock['dilute'] - 1,
             linewidth=fig_config["line_width"], label='Dilute')
ax1.semilogy(altitude, index_post_shock['dilute'] - 1,
             linewidth=fig_config["line_width"], label='Dense')

ax1.set_xlabel('Altitude $[m]$', fontsize=fig_config["axis_label_size"])
ax1.set_ylabel('n - 1 $[ ]$', fontsize=fig_config["axis_label_size"])
ax1.legend(fontsize=fig_config["legend_size"])

ax2 = ax1.twiny()
ax2.set_xlim(ax1.get_xlim())

# Set ticks to match ax1's temperature ticks, but label with density values
temp_ticks = ax1.get_xticks()
ax2.set_xticks(temp_ticks)
ax2.set_xticklabels([f"{rho:.4f}" for rho in np.interp(temp_ticks,
                                                       altitude, density_2)])

ax2.set_xlabel(r'$\rho$ [kg/m$^3$]', fontsize=fig_config["axis_label_size"])
plt.savefig(f'dilute_dense_altitude_{wavelength_nm}.pdf', format="pdf", bbox_inches="tight",
            dpi=fig_config["dpi_size"])
