import pickle
import haot
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import IPython
import os

def plot_stagnation_fields(data_in, fig_config, out_pdf_fig, cut_dict=None):
    case_names = ['1R', '2R', '3R']
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

        plt.xticks(fontsize=fig_config['ticks_size'])
        plt.yticks(fontsize=fig_config['ticks_size'])

        if cut_dict and 'temperature' in cut_dict[n]:
            plt.xlim(cut_dict[n]['temperature'])
        plt.savefig(os.path.join(out_pdf_fig, f'{n}_temperatures.pdf'),
                    format='pdf', bbox_inches='tight',
                    dpi=fig_config['dpi_size'])
        plt.close() 

def get_cut_dict():
    cut_dict = { }
    cut_dict['1R'] = {
            'temperature': [-2.5, 0]
            }

    cut_dict['2R'] = {
            'temperature': [-2.5, 0]
            }

    cut_dict['3R'] = {
            'temperature': [-2.5, 0]
            }
    return cut_dict


if __name__ == "__main__":

    out_pdf_fig = "../figures/chapter5/chemistryReaction"
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

    cut_dict = get_cut_dict()

    file = open(pickle_path, 'rb')
    data_in = pickle.load(file)

    plot_stagnation_fields(data_in, fig_config, out_pdf_fig, cut_dict)


