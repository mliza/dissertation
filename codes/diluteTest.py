import numpy as np
import matplotlib.pyplot as plt
import figure_configurations


index_refraction = np.linspace(1, 1.1, 5000)
dilute = index_refraction - 1
dense = (index_refraction**2 - 1) / (index_refraction**2 + 2)
fig_config = figure_configurations.figure_settings()
fig = plt.figure(figsize=(fig_config["fig_width"], fig_config["fig_height"]))

plt.semilogy(index_refraction, dilute,  linewidth=fig_config["line_width"], label=
         'Dilute')
plt.semilogy(index_refraction, dense,  linewidth=fig_config["line_width"], label=
         'Dense')
#plt.plot(index_refraction, dense - index_refraction)
plt.xlabel('n  $[ ]$', fontsize=fig_config["axis_label_size"])
plt.ylabel('n - 1 $[ ]$', fontsize=fig_config["axis_label_size"])
plt.legend(fontsize=fig_config["legend_size"])
plt.show()
"""
plt.savefig('dilute_dense_delta.pdf', format="pdf", bbox_inches="tight",
            dpi=fig_config["dpi_size"])
"""


