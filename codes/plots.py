#!/opt/homebrew/bin/python3.9
'''
    Date:   11/13/2021
    Author: Martin E. Liza
    File:   project_2.py
    Def:

    Author		Date		Revision
    ----------------------------------------------------
    Martin E. Liza	11/13/2021	Initial version.
'''
import numpy as np
import matplotlib.pyplot as plt 
from ambiance import Atmosphere 
import pandas as pd 
import matplotlib.pyplot as plt 
import os 
import IPython

#def temperature_ratio_plot(ratio_1, ratio_2, ratio_3, velocity):
def temperature_ratio_plot(data_path):
    perfect_gas = pd.read_csv(os.path.join(data_path,
                                           'calorically_perfect.csv'))
    e1 = pd.read_csv(os.path.join(data_path, '1e-1atm.csv')) 
    e2 = pd.read_csv(os.path.join(data_path, '1e-2atm.csv')) 
    e4 = pd.read_csv(os.path.join(data_path, '1e-4atm.csv')) 

    # Plotting 
    plt.plot(perfect_gas['U'], perfect_gas['T_ratio'],
            label='Calorically perfect gas', linewidth='2')

    plt.plot(e1['U'] , e1['T_ratio'],
            label='$1e^{-1}\,[atm],\;h=16.1[km]$', linewidth='2')

    plt.plot(e2['U'] , e2['T_ratio'],
            label='$1e^{-2}\,[atm],\;h=31[km]$', linewidth='2')

    plt.plot(e4['U'] , e4['T_ratio'],
            label='$1e^{-4}\,[atm],\;h=64.858[km]$', linewidth='2')

    plt.legend() 
    plt.xlabel('$U_1\,[km/s]$')
    plt.ylabel('$T_2/T_1\,[\;]$')
    plt.savefig("temperatureRatio.png", format='png', bbox_inches='tight',
                dpi=600)
    plt.close()


if __name__ == "__main__":
    temperature_ratio_plot(data_path="calloricallyPerfectGasData")
