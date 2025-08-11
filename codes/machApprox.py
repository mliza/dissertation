import numpy as np
import matplotlib.pyplot as plt


def calculate_mach(temperatureK, pressureP, gamma, staticPressure=101.3):
    p_r = pressureP / staticPressure
    gamm_1 = gamma - 1

    return np.sqrt((2/gamm_1) * (p_r**(gamm_1/gamma) - 1))
    

if __name__ == "__main__":
    gamma_O2 = 1.2
    gamma_air = 1.4
    gamma_N2 = 1.1
    c_1 = calculate_mach(20000, 2760, gamma_air)
    c_2 = calculate_mach(10000, 1380, gamma_O2)
    c_3 = calculate_mach(15000, 2067, gamma_air)
    s_11 = calculate_mach(15000, 2067, gamma_air)
    s_12 = calculate_mach(8000, 1000, gamma_air)

    print(f"1C Mach: {c_1}")
    print(f"2C Mach: {c_2}")
    print(f"3C Mach: {c_3}")
    print(f"1S1 Mach: {s_11}")
    print(f"1S2 Mach: {s_12}")
