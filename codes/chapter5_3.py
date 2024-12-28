import pickle
import haot
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import IPython

def plot_stagnation_fields(data_in, fig_config):
    case_names = ['1R', '2R', '3R']
    case_names = ['1R'] 
    blue = mcolors.TABLEAU_COLORS['tab:blue']
    orange = mcolors.TABLEAU_COLORS['tab:orange']

    for n in case_names:
        frozen = data_in[f'{n}_frozen_stagnation']
        noneq = data_in[f'{n}_nonequilibrium_stagnation']

        plt.plot(frozen['x'] * 1E3, frozen['Temperature_tr'], color=blue,
            linewidth=fig_config['line_width'], label='$T_{tr}$')
        plt.plot(frozen['x'] * 1E3, frozen['Temperature_ve'], color=orange,
            linewidth=fig_config['line_width'], label='$T_{vib}$')

        plt.plot(noneq['x'] * 1E3, noneq['Temperature_tr'], '-.', color=blue,
            linewidth=fig_config['line_width'])
        plt.plot(noneq['x'] * 1E3, noneq['Temperature_ve'], '-.', color=orange,
            linewidth=fig_config['line_width'])
        plt.legend(fontsize=fig_config['legend_size'])
        plt.xlabel('X $[mm]$', fontsize=fig_config['axis_label_size'])
        plt.ylabel('T $[K]$', fontsize=fig_config['axis_label_size'])
        plt.xticks(fontsize=fig_config['legend_size'])
        plt.yticks(fontsize=fig_config['legend_size'])
        plt.show() 


if __name__ == "__main__":

    pickle_path = "../resultsCFD/chemistryReaction/tecOutData/stagnation.pickle"
    fig_config = {}
    fig_config["line_width"] = 3
    fig_config["fig_width"] = 6
    fig_config["fig_height"] = 5
    fig_config["dpi_size"] = 600
    fig_config["axis_label_size"] = 14
    fig_config["legend_size"] = 12
    fig_config["ticks_size"] = 13
    fig_config["title_size"] = 18

    file = open(pickle_path, 'rb')
    data_in = pickle.load(file)

    plot_stagnation_fields(data_in, fig_config)


