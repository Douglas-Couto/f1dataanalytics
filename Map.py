import fastf1 as f1
import matplotlib
from fastf1 import utils
from fastf1 import plotting
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.collections import LineCollection
from matplotlib import cm
import numpy as np
import pandas as pd

# Enable cache
f1.Cache.enable_cache('cache')

#setup plotting
plotting.setup_mpl(mpl_timedelta_support=True, color_scheme='fastf1', misc_mpl_mods=True)

#Getting the data
bahrain_2022 = f1.get_session(2022, 1, 'Q')
laps = bahrain_2022.load_laps(with_telemetry=True)

#Fastest lap for each driver during qualy
lec_lap = laps.pick_driver('16').pick_fastest().get_telemetry().add_distance()
ham_lap = laps.pick_driver('44').pick_fastest().get_telemetry().add_distance()

#Points for GPS tracking
x = np.array(lec_lap['X'].values)
y = np.array(lec_lap['Y'].values)


#Giving each driver a name
lec_lap['Driver'] = 'LEC'
ham_lap['Driver'] = 'HAM'

#Coupling data in a single table
telemetry = lec_lap.append(ham_lap)

#Number of minisectors
n_minisectors = 200

#Minisectors Lenght
total_distance = total_distance = max(telemetry['Distance'])
mini_lenght = total_distance/n_minisectors

#initiating array minisectors
minisectors = [0]

#Creating the column minisector and adding to each row in the data
for i in range(0, n_minisectors - 1):
    minisectors.append(mini_lenght*(i+1))

telemetry['Minisector'] = telemetry['Distance'].apply(
    lambda dist: (
        int((dist // mini_lenght) + 1)
    )
)

average_speed = telemetry.groupby(['Minisector', 'Driver'])['Speed'].mean().reset_index()

fastest_driver = average_speed.loc[average_speed.groupby(['Minisector'])['Speed'].idxmax()]
fastest_driver = fastest_driver[['Minisector','Speed','Driver']].rename(columns={'Driver': 'FastestDriver'})


telemetry = telemetry.merge(fastest_driver, on=['Minisector'])

telemetry = telemetry.sort_values(by=['Distance'])

telemetry.loc[telemetry['FastestDriver'] == 'HAM', 'Fastest_driver_int'] = 1
telemetry.loc[telemetry['FastestDriver'] == 'LEC', 'Fastest_driver_int'] = 2

#Points into segments
points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
fastest_driver_array = telemetry['Fastest_driver_int'].to_numpy().astype(float)

cmap = cm.get_cmap('cool',2)
lc_comp = LineCollection(segments, norm=plt.Normalize(1, cmap.N+1), cmap=cmap)
lc_comp.set_array(fastest_driver_array)
lc_comp.set_linewidth(5)

plt.rcParams['figure.figsize'] = [18, 10]

plt.gca().add_collection(lc_comp)
plt.axis('equal')
plt.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)

# cbar = plt.colorbar(mappable=lc_comp, boundaries=np.arange(1,4))
# cbar.set_ticks(np.arange(1.5, 9.5))
# cbar.set_ticklabels(['HAM', 'LEC'])

#teste = telemetry.groupby(['Minisector', 'Driver', 'FastestDriver', 'Fastest_driver_int'])

print(fastest_driver)
data = telemetry[['Minisector', 'Distance', 'Driver', 'FastestDriver', 'Fastest_driver_int']]

plt.show()



