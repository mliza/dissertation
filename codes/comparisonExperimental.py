import os
import haot
import IPython
import numpy as np
import matplotlib.pyplot as plt
import figure_configurations
import chapter5_12


def main(cfd_results_abs_path):
    fig_config = figure_configurations.figure_settings()
    species_flag = False

    data_in_path = os.path.join(
        cfd_results_abs_path, "chemistryComposition", "outputs"
    )
    files_in = ["4C.csv", "5C.csv"]

    optical_properties(
        data_in_path, files_in, output_png_path, fig_config, cut_dict_chemistry
    )

if __name__ == "__main__":
    cfd_results_abs_path = "../resultsCFD"
    main(cfd_results_abs_path)


