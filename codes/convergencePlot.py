import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import re
import figure_configurations
import IPython


# Clean input file
def load_csv(file_in: str, key_iter: str) -> dict:
    df = pd.read_csv(file_in)
    dict_out = {}
    fields = list(df.keys())
    #rms_keys = df.drop(columns=["Time_Iter", "Outer_Iter", "Inner_Iter"])
    dict_out[key_iter] = np.array(df[key_iter])


    #for i in fields[3:-10]:
    for i in fields[3:]:
        i_temp = i.strip().replace('"', "")
        match = re.match(r"(\w+)\[(\w+)", i_temp)
        clean_str = (f"{match.group(1)}_{match.group(2)}").strip("rms_")
        dict_out[clean_str] = np.array(df[i])

    return dict_out

def load_csv_old(file_in: str, key_iter: str) -> dict:
    df = pd.read_csv(file_in)
    dict_out = {}
    fields = list(df.keys())
    #rms_keys = df.drop(columns=["Time_Iter", "Outer_Iter", "Inner_Iter"])
    dict_out[key_iter] = np.array(df[key_iter])


    for i in fields[3:-10]:
        i_temp = i.strip().replace('"', "")
        match = re.match(r"(\w+)\[(\w+)", i_temp)
        clean_str = (f"{match.group(1)}_{match.group(2)}").strip("rms_")
        dict_out[clean_str] = np.array(df[i])

    return dict_out


# Plot RMS
def plot_rms(dict_data: str, key_iter: str, key_in: str = False, figh_config=None):
    if fig_config['out_path'].split('/')[1].split('_')[1] == 'nonequilibrium':
        species = ["N", "O", "NO", "N2", "O2"]
        fields = [k for k in dict_data if k != key_iter][:5]
    else:
        species = ["N2", "O2"]
        fields = [k for k in dict_data if k != key_iter][3:5]

    fig = plt.figure(figsize=(fig_config["fig_width"], fig_config["fig_height"]))
    for indx, key in enumerate(fields):
        plt.plot(
            dict_data[key_iter],
            dict_data[key],
            linewidth=fig_config["line_width"],
            label=figure_configurations.rename_label(species[indx]),
        )

    plt.legend(fontsize=fig_config["legend_size"])
    plt.ylabel("RMS", fontsize=fig_config["axis_label_size"])
    plt.xlabel("Number of Iterations", fontsize=fig_config["axis_label_size"])

    if "out_path" in fig_config:
        plt.tight_layout()
        plt.savefig(
            fig_config["out_path"],
            format="pdf",
            bbox_inches="tight",
            dpi=fig_config["dpi_size"],
        )
        plt.close()
    else:
        plt.show()


if __name__ == "__main__":
    path_r = "/Users/martin/Documents/Schools/UoA/Dissertation/resultsCFD/chemistryReaction/R_files"
    path_r = "/Users/martin/Desktop/mackey/R_files"
    path_r = "/Users/martin/Desktop/R_files"
    cases_in = os.listdir(path_r)
    fig_config = figure_configurations.figure_settings()
    key_iter = "Inner_Iter"
    key_in = False
    out_path = "tmp2"
    for i in cases_in:
        fig_config['out_path'] = os.path.join(out_path, f'{i}_convergence.pdf')
        dict_data = load_csv(os.path.join(path_r, i, "history.csv"), key_iter)
        dict_data_old = load_csv_old(os.path.join(path_r, i, "history1.csv"), key_iter)
        plot_rms(dict_data, key_iter, key_in, fig_config)
