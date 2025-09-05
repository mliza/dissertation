import numpy as np
import matplotlib.pyplot as plt
import figure_configurations
import haot
import IPython


index_refraction = np.linspace(1, 2, 10000)
temperature_K = np.linspace(100, 50000, 1000)
pressure_Pa = 1E6
wavelength_nm = 1000 
gas_constant = 287.058
mass_density = pressure_Pa / (gas_constant * temperature_K)


dilute = index_refraction - 1
dense = (index_refraction**2 - 1) / (index_refraction**2 + 2)

kerl_polarizability = haot.kerl_polarizability_temperature(temperature_K,
                                                           "Air", wavelength_nm)

index = haot.index_of_refraction_density_temperature(temperature_K, mass_density,
                                             "Air", wavelength_nm)

# Plot n(T, pro)
fig_config = figure_configurations.figure_settings()
fig, ax1 = plt.subplots(figsize=(fig_config["fig_width"] + 2, fig_config["fig_height"]))
# First plot: temperature vs n-1
ax1.semilogy(temperature_K, index['dilute'] - 1, linewidth=fig_config["line_width"],
             label='Dilute')
ax1.semilogy(temperature_K, index['dense'] - 1, linewidth=fig_config["line_width"],
             label='Dense')

# Axis labels
ax1.set_xlabel('T $[K]$', fontsize=fig_config["axis_label_size"])
ax1.set_ylabel('n - 1 $[ ]$', fontsize=fig_config["axis_label_size"])
ax1.legend(fontsize=fig_config["legend_size"])

# Second x-axis: density
ax2 = ax1.twiny()
ax2.set_xlim(ax1.get_xlim())

# Set ticks to match ax1's temperature ticks, but label with density values
temp_ticks = ax1.get_xticks()
ax2.set_xticks(temp_ticks)
ax2.set_xticklabels([f"{rho:.3f}" for rho in np.interp(temp_ticks, temperature_K, mass_density)])

ax2.set_xlabel(r'$\rho$ [kg/m$^3$]', fontsize=fig_config["axis_label_size"])


plt.savefig(f'dilute_dense_pressure_{pressure_Pa:.0E}.pdf', format="pdf", bbox_inches="tight",
            dpi=fig_config["dpi_size"])
plt.close()



fig = plt.figure(figsize=(fig_config["fig_width"], fig_config["fig_height"]))

plt.semilogy(index_refraction, dilute,  linewidth=fig_config["line_width"], label=
         'Dilute')
plt.semilogy(index_refraction, dense,  linewidth=fig_config["line_width"], label=
         'Dense')
#plt.plot(index_refraction, dense - index_refraction)
plt.xlabel('n  $[ ]$', fontsize=fig_config["axis_label_size"])
plt.ylabel('n - 1 $[ ]$', fontsize=fig_config["axis_label_size"])
plt.legend(fontsize=fig_config["legend_size"])
plt.savefig('dilute_dense_delta.pdf', format="pdf", bbox_inches="tight",
            dpi=fig_config["dpi_size"])

