import haot
import numpy as np
import matplotlib.pyplot as plt
import IPython 

def test_buldakov_method(vibrational_number, rotational_number, fig_config=None, output_png=None,
                    test_formulation=None):

    molecule = ['H2', 'N2', 'O2']
    temperature_K = np.arange(100, 2000, 50)
    vib_axis = range(vibrational_number + 1)
    rot_axis = range(rotational_number + 1)
    buldakov_dict = { }
    buldakov_dict['temperature_K'] = temperature_K
    buldakov_dict['kerl'] = {} 

    for k in molecule:
        buldakov = np.zeros([np.size(temperature_K)])
        expansion = np.zeros([vibrational_number + 1,
                            rotational_number + 1])
        distribution = np.zeros([np.size(temperature_K),
                                 vibrational_number + 1,
                                 rotational_number + 1])
        for j in rot_axis:
            for v in vib_axis:
                expansion[v,j] = haot.buldakov_expansion(
                                vibrational_number=v,
                                rotational_number=j,
                                molecule=k) 
                if test_formulation:
                    expansion[v,j] -= haot.buldakov_polarizability_derivatives_2016(k)['zeroth']
                    expansion[v,j] += haot.kerl_interpolation(k)['groundPolarizability']

        # Probability Distribution
        for t, val in enumerate(temperature_K):
            distribution[t] = haot.boltzmann_distribution(val, k, 
                                                vibrational_number,
                                                rotational_number, False
                                                    ).reshape(vibrational_number+ 1, 
                                                            rotational_number + 1)
            buldakov[t] = np.sum(distribution[t] * expansion)

        buldakov_dict[k] = buldakov

    if not fig_config:
        return buldakov_dict

if __name__ == "__main__":
    #vibrationa,rotational buld_v

    #bul_00 = test_buldakov_method(0,0)
    #bul_01 = test_buldakov_method(0,1)
    #bul_10 = test_buldakov_method(1,0)
    bul_11 = test_buldakov_method(1,1, fig_config=None, output_png=None,
                                  test_formulation=True)

    bul_12 = test_buldakov_method(1,2)
    bul_13 = test_buldakov_method(1,3)
    mol = 'N2'


    #plt.plot(bul_00['temperature_K'], bul_00[mol], label=f'{mol} 00')
    plt.plot(bul_11['temperature_K'], bul_11[mol], label=f'{mol} 11')
    plt.plot(bul_12['temperature_K'], bul_12[mol], label=f'{mol} 12')
    plt.plot(bul_13['temperature_K'], bul_13[mol], label=f'{mol} 13')
    plt.legend()
    plt.show() 


