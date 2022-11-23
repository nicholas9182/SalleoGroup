import plumed as pl
import matplotlib.pyplot as plt
from analysis.metadynamics.free_energy import FreeEnergyLandscape

"""
First part tries out the plotting routine
"""


def plot_hills(df):
    plt.plot(df['time'], df['height'])


hills1 = (pl.read_as_pandas("/Users/nicholassiemons/Dropbox/OBT/0085/004/HILLS_test")
          .groupby('time', group_keys=True)
          .apply(lambda x: x.assign(walker=lambda y: range(0, y.shape[0])))
          .query('walker == 0')
          # .pipe(plot_hills)
          )

"""
Second part tries out the code in the package
"""
hills2 = pl.read_as_pandas("/Users/nicholassiemons/Dropbox/OBT/0085/004/HILLS_test")
landscape = FreeEnergyLandscape(hills2)
figures = landscape.get_hills_figures(round_time=2)

for key, value in figures.items():
    save_dir = "/Users/nicholassiemons/Dropbox/OBT/0085/Summary/Figures/Walkers_004/Walker_" + str(key) + ".pdf"
    value.write_image(save_dir)
