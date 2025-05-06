from haot import aerodynamics
from haot import optics
from haot import quantum_mechanics
from haot import constants
from haot import conversions
from ambiance import Atmosphere
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator 
from matplotlib.patches import Patch
from mpl_toolkits.mplot3d import Axes3D

import IPython


def test_aerodynamics_module(fig_config='None', output_png='None'):
    altitude = np.linspace(0, 81e3, num=200)
    atmosphere = Atmosphere(altitude)
    atmo_dynamic_visc = atmosphere.dynamic_viscosity

    # Calculating dynamic viscosity and speed of sound 
    haot_dynamic_visc = aerodynamics.sutherland_law_viscosity(atmosphere.temperature)
    haot_speed_of_sound = aerodynamics.speed_of_sound(atmosphere.temperature)

    if fig_config: 
        fix, axs = plt.subplots(1,2, figsize=(fig_config["fig_width"] + 2,
                                              fig_config["fig_height"]),
                                    dpi=fig_config["dpi_size"])

        axs[0].plot(haot_speed_of_sound, altitude*1E-3, linewidth=
                      fig_config["line_width"], label='HAOT')
        axs[0].plot(atmosphere.speed_of_sound, altitude*1E-3, '-.', linewidth=
                      fig_config["line_width"], label='Ambiance')
        axs[0].set_xlabel('Speed of Sound $[m/s]$',
                          fontsize=fig_config["axis_label_size"])
        axs[0].set_ylabel('Altitude $[km]$',
                          fontsize=fig_config["axis_label_size"])
        axs[0].legend(fontsize=fig_config['legend_size'])

        axs[1].plot(haot_dynamic_visc, altitude*1E-3, linewidth=
                      fig_config["line_width"], label='HAOT')
        axs[1].plot(atmosphere.dynamic_viscosity, altitude*1E-3, '-.', linewidth=
                      fig_config["line_width"], label='Ambiance')
        axs[1].set_xlabel('Dynamic Viscosity $[Pa\,s]$',
                          fontsize=fig_config["axis_label_size"])
        axs[1].set_ylabel('Altitude $[km]$',
                          fontsize=fig_config["axis_label_size"])
        axs[1].legend(fontsize=fig_config['legend_size'])
        
        if output_png is not None: 
            plt.tight_layout()
            plt.savefig(os.path.join(output_png,'aerodynamics.pdf'),
                        format='pdf',
                bbox_inches='tight', dpi=fig_config["dpi_size"])
            plt.close()

        if output_png is None:
            plt.show()

    ## Oblique shockwaves 
    mach_number = np.linspace(0, 4, 200)
    deflection = [2,3,4]
    for i in deflection:
        haot.oblique_shock_angle(mach_number, i)
        # TODO: PLOT ME and update




def test_optics_module(fig_config=None, output_png=None, paper_data=None):
    keys = ['N2', 'O2', 'H2', 'Air']
    wavelength_nm = 633
    temperature_K = np.arange(100, 2000, 50)
    dict_kerl = { }
    dict_kerl['temperature_K'] = temperature_K

    for k in keys:
        dict_kerl[k] = np.zeros(np.shape(temperature_K)[0])
        for i, val in enumerate(temperature_K):
            dict_kerl[k][i] = optics.kerl_polarizability_temperature(val, k,
                                                                wavelength_nm)
    if not fig_config:
        return dict_kerl

    if fig_config:
        fig = plt.figure(figsize=(fig_config['fig_width'],
                                      fig_config['fig_height']))
        for k in keys:
            plt.plot(temperature_K, dict_kerl[k],
                    linewidth=fig_config['line_width'], 
                     label='HAOT')

            if paper_data and (k != 'Air'):
                plt.plot(paper_data[f'kerl_{k}']['temperature_K'],
                         paper_data[f'kerl_{k}']['polarizability_m3'],
                         '-.', linewidth=fig_config['line_width'],
                         label='Kerl')
                plt.legend(fontsize=fig_config['legend_size'])

            if k == 'O2':
                plt.xlim([100, 1500])
                plt.ylim([np.min(paper_data[f'kerl_{k}']['polarizability_m3']),
                          np.max(paper_data[f'kerl_{k}']['polarizability_m3'])])
            else:
                plt.xlim([100, 2000])

            plt.xlabel('Temperature $[K]$',
                        fontsize=fig_config['axis_label_size'])
            plt.ylabel('Polarizability $[m^3]$',
                       fontsize=fig_config['axis_label_size'])

            ## Maybe Move this Out ##
            plt.xticks(fontsize=fig_config['ticks_size'])
            plt.yticks(fontsize=fig_config['ticks_size'])

            if output_png is not None:
                plt.savefig(os.path.join(output_png,
                f'kerlPolarizability_{k}_{wavelength_nm}nm.pdf'),
                        format = 'pdf',
                        bbox_inches='tight', dpi=fig_config['dpi_size'])
                plt.close()
            if output_png is None:
                plt.show()

def test_buldakov_method(fig_config=None, output_png=None):
    molecule = ['H2', 'N2', 'O2']
    temperature_K = np.arange(100, 2000, 50)
    vibrational_number = 1 
    rotational_number = 2
    vib_axis = range(vibrational_number + 1)
    rot_axis = range(rotational_number + 1)
    buldakov_dict = { }
    buldakov_dict['temperature_K'] = temperature_K

    for k in molecule:
        buldakov = np.zeros([np.size(temperature_K)])
        expansion = np.zeros([vibrational_number + 1,
                            rotational_number + 1])
        distribution = np.zeros([np.size(temperature_K),
                                 vibrational_number + 1,
                                 rotational_number + 1])
        for j in rot_axis:
            for v in vib_axis:
                expansion[v,j] = optics.buldakov_expansion(
                                vibrational_number=v,
                                rotational_number=j,
                                molecule=k)

        # Probability Distribution
        for t, val in enumerate(temperature_K):
            distribution[t] = quantum_mechanics.boltzmann_distribution( 
                                                val, k, 
                                                vibrational_number,
                                                rotational_number, False)

            buldakov[t] = np.sum(distribution[t] * expansion)

        buldakov_dict[k] = buldakov

    if not fig_config:
        return buldakov_dict
        
    if fig_config:
        for k in molecule:
            fig = plt.figure(figsize=(fig_config['fig_width'],
                                      fig_config['fig_height']))
            plt.plot(temperature_K, buldakov_dict[k],
                    linewidth=fig_config['line_width'])

            plt.xlabel('Temperature $[K]$',
                        fontsize=fig_config['axis_label_size'])
            plt.ylabel('Polarizability $[m^3]$',
                       fontsize=fig_config['axis_label_size'])

            ## Maybe Move this Out ##
            #plt.legend(fontsize=fig_config['legend_size'])
            plt.xticks(fontsize=fig_config['ticks_size'])
            plt.yticks(fontsize=fig_config['ticks_size'])

            if output_png:
                plt.savefig(os.path.join(output_png,
                    f'buldakovPolarizability_{k}.pdf'), format = 'pdf',
                    bbox_inches='tight', dpi=fig_config['dpi_size'])
                plt.close()
            else:
                plt.show()

def test_quantum_mechanics_module(fig_config=None, output_png=None):
    vibrational_number = 1 
    rotational_number = 40
    temperature_K = [100.0, 500.0, 1000.0]
    molecule = ['N2', 'O2', 'NO']
    elev_ang = 16
    azim_ang = 40
    vib_axis = range(vibrational_number + 1)
    rot_axis = range(rotational_number + 1)

    for k in molecule:
        # [temperature, vibrational, rotational]
        distribution = np.zeros([np.size(temperature_K),
                                 vibrational_number + 1,
                                 rotational_number + 1])
        for t, val in enumerate(temperature_K):
            distribution[t] = quantum_mechanics.boltzmann_distribution( 
                                                val, k, 
                                                vibrational_number,
                                                rotational_number, False)
        if fig_config:
            # Plots Distribution function
            vib_mesh, rot_mesh = np.meshgrid(vib_axis, rot_axis)
            fig, ax = plt.subplots(subplot_kw={"projection": "3d"},
                                   figsize=(fig_config['fig_width'],
                                            fig_config['fig_height']))
            # Color options 
            colormaps = ['viridis', 'plasma', 'cividis']

            # Plot tempeteratures
            for i, temp in enumerate(temperature_K):
                cmap = plt.get_cmap(colormaps[i])
                surf = ax.plot_surface(vib_mesh.T, rot_mesh.T, 
                                       distribution[i],
                                       cmap=cmap, edgecolor='k',
                                       alpha=0.8,
                                       linewidth=0.5)
                ax.text(x=vibrational_number // 2, 
                        y=rotational_number // (4 - i),
                        z=np.max(distribution[i]),
                        s=f'T = {temp} [K]', color='k', 
                        fontsize=fig_config['legend_size'])

            # Change grid and background colors
            ax.set_facecolor('white') 
            fig.patch.set_facecolor('white')
            ax.grid(False)
            ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0)) 
            ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
            ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))

            # 3D axis views
            ax.view_init(elev=elev_ang, azim=azim_ang)

            # Labels
            ax.set_xlabel('Vibrational # $[\;]$',
                           fontsize=fig_config['axis_label_size'])

            ax.set_ylabel('Rotational # $[\;]$',
                           fontsize=fig_config['axis_label_size'])

            ax.set_zlabel('Boltzmann Distribution $[\;]$',
                           fontsize=fig_config['axis_label_size'])

            # Integers for axis ticks
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))


            if output_png:
                plt.savefig(os.path.join(output_png,
                            f'boltzmannDistribution_{k}.pdf'), 
                            format = 'pdf',
                        bbox_inches='tight', 
                        pad_inches=0.3,
                        dpi=fig_config['dpi_size'])
                plt.close()
            else:
                plt.show()

            
def plot_buldakov_kerl(fig_config, output_png, paper_data=None,
                       field_key='kerl'):
    buldakov = test_buldakov_method()
    kerl = test_optics_module()
    keys = ['N2', 'O2', 'H2']

    for k in keys:
        fig = plt.figure(figsize=(fig_config['fig_width'],
                                  fig_config['fig_height']))
        plt.plot(kerl['temperature_K'], kerl[k],
                linewidth=fig_config['line_width'], 
                label='Kerl, HAOT')

        plt.plot(buldakov['temperature_K'], buldakov[k],
                linewidth=fig_config['line_width'], 
                label='HAOT')

        if k == 'O2':
            plt.xlim([100, 1500])
        else:
            plt.xlim([100, 2000])


        if paper_data:
            plt.plot(paper_data[f'{field_key}_{k}']['temperature_K'],
                     paper_data[f'{field_key}_{k}']['polarizability_m3'],
                     '-.', linewidth=fig_config['line_width'],
                     label=f'{field_key}, Paper')

        plt.xlabel('Temperature $[K]$',
                    fontsize=fig_config['axis_label_size'])
        plt.ylabel('Polarizability $[m^3]$',
                   fontsize=fig_config['axis_label_size'])

        ## Maybe Move this Out ##
        plt.xticks(fontsize=fig_config['ticks_size'])
        plt.yticks(fontsize=fig_config['ticks_size'])
        plt.legend(fontsize=fig_config['legend_size'])

        if output_png:
            plt.savefig(os.path.join(output_png,
                f'polarizabilityComparison_{k}.pdf'), format = 'pdf',
                bbox_inches='tight', dpi=fig_config['dpi_size'])
            plt.close()
        else:
            plt.show()

def load_paper_data(paper_data):
    files_in = os.listdir(paper_data)
    dict_out = { }
    for i in files_in:
        key = i.split('.')[0]
        df_in = pd.read_csv(os.path.join(paper_data, i))
        dict_out[key] = df_in.to_dict(orient='list')
    return dict_out

def plot_buldakov_buldakov(fig_config, buldakov_dict, buldakov_paper):
    calc_temp = buldakov_dict['temperature_K']
    keys = ['N2', 'O2', 'H2']
    
    for i in keys:
        plt.plot(buldakov_paper[f'buldakov_{i}']['temperature_K'],
                 buldakov_paper[f'buldakov_{i}']['polarizability_m3'],
                      linewidth=fig_config['line_width'],
                 label='Buldakov')
        plt.plot(calc_temp, buldakov_dict[f'{i}'], 
                     '-.', linewidth=fig_config['line_width'],
                    label='HAOT')
        if i == 'O2':
            plt.xlim([100, 1500])
        else:
            plt.xlim([100, 2000])

        plt.xlabel('Temperature $[K]$',
                    fontsize=fig_config['axis_label_size'])
        plt.ylabel('Polarizability $[m^3]$',
                   fontsize=fig_config['axis_label_size'])


        plt.legend(fontsize=fig_config['legend_size'])
        plt.savefig(os.path.join(output_png,
            f'buldakovHAOT_{i}.pdf'), format = 'pdf',
            bbox_inches='tight', dpi=fig_config['dpi_size'])
        plt.close()




if __name__ == "__main__":
    fig_config = {}
    fig_config['line_width'] = 3
    fig_config['fig_width'] = 6
    fig_config['fig_height'] = 5
    fig_config['dpi_size'] = 600
    fig_config['axis_label_size'] = 14
    fig_config['legend_size'] = 12
    fig_config['ticks_size'] = 13
    fig_config["title_size"] = 18
    output_png = "figures"
    output_png = "../figures/chapter4"
    paper_csv = "buldakovPaper"

    paper_data = load_paper_data(paper_csv) 
    kerl_data = load_paper_data("kerlPaper") 
    test_aerodynamics_module(fig_config, output_png)
    test_quantum_mechanics_module(fig_config, output_png) 
    test_buldakov_method(fig_config, output_png)
    buldakov_dict = test_buldakov_method( )
    plot_buldakov_kerl(fig_config, output_png, paper_data, 'buldakov')
    plot_buldakov_buldakov(fig_config, buldakov_dict, paper_data)
    test_optics_module(fig_config, output_png, kerl_data)
