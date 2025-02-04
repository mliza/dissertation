import pyvista as pv
import haot
import os 
import sys
import IPython

# SU2 [N, O, NO, N2, O2]
def load_files(files_in_path):
    dict_out = { }
    for i in os.listdir(files_in_path):
        reader = pv.get_reader(os.path.join(files_in_path, i, 'flow.vtu'))
        dict_out[i] = reader.read()
    return dict_out


def create_mass_density(mesh_in, species):
    IPython.embed(colors = "Linux")
    for i in mesh_in:
        i.point_data_to_cell_data()
        for i, val in enumerate(especies):

def main(mesh_data, fig_config):
    pass



if __name__ == "__main__":
    abs_path = (
    "/Users/martin/Documents/Schools/UoA/Dissertation/resultsCFD/chemistryReaction"
    )
    files_in = os.path.join(abs_path, 'R_files')


    # Users inputs #
    fig_config = {}
    fig_config["line_width"] = 3
    fig_config["fig_width"] = 6
    fig_config["fig_height"] = 5
    fig_config["dpi_size"] = 600
    fig_config["axis_label_size"] = 14
    fig_config["legend_size"] = 12
    fig_config["ticks_size"] = 13
    fig_config["title_size"] = 18

    species = ["N", "O", "NO", "N2", "O2"]

    mesh_data = load_files(files_in)
    density_dict = create_mass_density(mesh_data, species)



    main(mesh_data, fig_config)

