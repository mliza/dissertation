import os
import haot
import IPython
import numpy as np
import matplotlib.pyplot as plt
import figure_configurations
import chapter5_12
import pandas as pd


def main(cfd_results_abs_path, exp_data_path):
    fig_config = figure_configurations.figure_settings()
    species_flag = False

    data_in_path = os.path.join(
        cfd_results_abs_path, "chemistryComposition", "outputs"
    )
    files_in = ["4C.csv", "5C.csv"]

    output_png_path = 'tmp'
    cut_dict_chemistry = { }
    data_in = chapter5_12.optical_properties(
        data_in_path, files_in, output_png_path, fig_config, cut_dict_chemistry
    )
    experimental_4C = pd.read_csv(os.path.join(exp_data_path, '4C_paper_data.csv'))
    experimental_5C = pd.read_csv(os.path.join(exp_data_path, '5C_paper_data.csv'))



    fig, axes = plt.subplots(1, 2, figsize=(fig_config["fig_width"] + 5, fig_config["fig_height"]))


    axes[0].semilogx(data_in['4C']['temperature']['time'],
                 (data_in['4C']['refraction_index']['dilute'] - 1) * 1E4,
                 linewidth=fig_config["line_width"],
                 label='HAOT, dilute')
    axes[0].semilogx(data_in['4C']['temperature']['time'],
                 (data_in['4C']['refraction_index']['dense'] - 1) * 1E4, '--',
                 linewidth=fig_config["line_width"],
                 label='HAOT, dense')

    axes[1].semilogx(experimental_4C['time'] - experimental_4C['time'][0],
                 experimental_4C['index'] * 1E4, linewidth=fig_config["line_width"],
                 label='Experimental')

    axes[0].legend(fontsize=fig_config["legend_size"])
    axes[1].legend(fontsize=fig_config["legend_size"])

    axes[0].set_xlabel("Time $[s]$", fontsize=fig_config["axis_label_size"])
    axes[1].set_xlabel("Time $[s]$", fontsize=fig_config["axis_label_size"])

    axes[0].set_ylabel("$(n- 1) \\times 10^4$ $[\;]$",
                       fontsize=fig_config["axis_label_size"])
    axes[1].set_ylabel("$(n- 1) \\times 10^4$ $[\;]$",
                       fontsize=fig_config["axis_label_size"])


    plt.show() 
                                                                



    

    

if __name__ == "__main__":
    cfd_results_abs_path = "../resultsCFD"
    exp_data_path = '/Users/martin/Desktop'
    main(cfd_results_abs_path, exp_data_path)


