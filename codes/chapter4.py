from haot import aerodynamics
from haot import optics
from haot import constants
from haot import conversions
from ambiance import Atmosphere
import numpy as np
import os
import matplotlib.pyplot as plt


import IPython


def test_aerodynamics_module(fig_config='None', output_png='None'):
    altitude = np.linspace(0, 81e3, num=200)
    atmosphere = Atmosphere(altitude)
    atmo_dynamic_visc = atmosphere.dynamic_viscosity

    # Calculating dynamic viscosity and speed of sound 
    haot_dynamic_visc = aerodynamics.sutherland_law_viscosity(atmosphere.temperature)
    haot_speed_of_sound = aerodynamics.speed_of_sound(atmosphere.temperature)

    if fig_config: 
        fix, axs = plt.subplots(1,2, figsize=(fig_config["fig_width"],
                                              fig_config["fig_height"]),
                                    dpi=fig_config["dpi_size"])

        axs[0].plot(atmosphere.speed_of_sound, altitude*1E-3, linewidth=
                      fig_config["line_width"], label='Ambiance')
        axs[0].plot(haot_speed_of_sound, altitude*1E-3, '--', linewidth=
                      fig_config["line_width"], label='HAOT')
        axs[0].set_ylabel('Speed of Sound $[m/s]$',
                          fontsize=fig_config["axis_label_size"])
        axs[0].set_xlabel('Altitude $[km]$',
                          fontsize=fig_config["axis_label_size"])
        axs[0].legend()

        axs[1].plot(atmosphere.dynamic_viscosity, altitude*1E-3, linewidth=
                      fig_config["line_width"], label='Ambiance')
        axs[1].plot(haot_dynamic_visc, altitude*1E-3, '--', linewidth=
                      fig_config["line_width"], label='HAOT')
        axs[1].set_ylabel('Dynamic Viscosity $[Pa\,s]$',
                          fontsize=fig_config["axis_label_size"])
        axs[1].set_xlabel('Altitude $[km]$',
                          fontsize=fig_config["axis_label_size"])
        axs[1].legend()
        
        if output_png: 
            plt.tight_layout()
            plt.savefig(os.path.join(output_png,'aerodynamics.png'), format='png',
                bbox_inches='tight', dpi=fig_config["dpi_size"])
            plt.close()

        if not output_png:
            plt.show()

def test_optics_module(fig_config='None', output_png='None'):
    keys = ['N2', 'O2', 'Air']
    wavelength_nm = 633
    temperature_K = np.linspace(200, 1500, 200) 
    dict_kerl = { }

    for k in keys:
        dict_kerl[k] = np.zeros(np.shape(temperature_K)[0])
        for i, val in enumerate(temperature_K):
            dict_kerl[k][i] = optics.kerl_polarizability_temperature(val, k,
                                                                wavelength_nm)

    if fig_config:
        fig = plt.figure(figsize=(fig_config['fig_width'],
                                      fig_config['fig_height']))
        for k in keys:
            plt.plot(temperature_K, dict_kerl[k],
                    linewidth=fig_config['line_width'], label=k)

        plt.xlabel('Temperature $[K]$',
                    fontsize=fig_config['axis_label_size'])
        plt.ylabel('Polarizability $[m^3]$',
                   fontsize=fig_config['axis_label_size'])

        ## Maybe Move this Out ##
        plt.legend(fontsize=fig_config['legend_size'])
        plt.xticks(fontsize=fig_config['ticks_size'])
        plt.yticks(fontsize=fig_config['ticks_size'])
        plt.savefig(os.path.join(output_png,
            f'kerlPolarizability_{wavelength_nm}nm.png'), format = 'png',
                    bbox_inches='tight', dpi=fig_config['dpi_size'])
        plt.close()



if __name__ == "__main__":
    fig_config = {}
    fig_config['line_width'] = 3
    fig_config['fig_width'] = 8
    fig_config['fig_height'] = 5
    fig_config['dpi_size'] = 600
    fig_config['axis_label_size'] = 15
    fig_config['legend_size'] = 12
    fig_config['ticks_size'] = 10
    fig_config["title_size"] = 18
    output_png = "figures"
    output_png = "../figures/chapter4"

    test_aerodynamics_module(fig_config, output_png)

    test_optics_module(fig_config, output_png)






