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

preseasonb_day3 = f1.get_testing_session(2022, 2, 3)
bahrain_2021 = f1.get_session(2021, 1, 'R')

laps = preseasonb_day3.load_laps(with_telemetry=True)
laps_old = bahrain_2021.load_laps(with_telemetry=True)
maxd, mind = 4000, 4500



ver2022 = laps.pick_driver('1').pick_fastest()
ver2021 = laps_old.pick_driver('VER').pick_fastest()


newlap = laps.pick_driver('1').pick_fastest().get_car_data().add_distance()
oldlap = laps_old.pick_driver('VER').pick_fastest().get_car_data().add_distance()
colormap = matplotlib.cm.plasma


# ham_laps.loc[ham_laps['Brake'] > 0, 'CurrentAction'] = 'Brake'
# ham_laps.loc[ham_laps['Throttle'] > 0, 'CurrentAction'] = 'Throttle'
# ham_laps.loc[ham_laps['Throttle'] == 100, 'CurrentAction'] = 'WOT'


# data = pd.DataFrame(ham_laps)
# data.to_excel(r'C:\Users\GAMER\PycharmProjects\f1Project\HamLapBahrain3.xlsx', index = False)
# print(data)

rbr_color = f1.plotting.team_color('RBR')
sec_color = f1.plotting.team_color('FER')
merc_color = f1.plotting.team_color('MER')


fig, ax = plt.subplots(2)

delta_time, ref_tel, compare_tel = utils.delta_time(ver2022, ver2021)


ax[1].plot(ref_tel['Distance'], delta_time, '--', color='white', label='2022 Pre season fastest')

ax[0].plot(oldlap['Distance'], oldlap['Speed'], color=sec_color, label='2021 Race Fastest')
ax[0].plot(newlap['Distance'], newlap['Speed'], color=rbr_color, label='2022 Pre season fastest')

ax[1].set_xlabel('Distance in m')
ax[1].set_ylabel("<-- Lec ahead | Ham ahead -->")
ax[0].set_ylabel('Speed in km/h')

ax[1].legend()
plt.suptitle(f"Fastest Lap Comparison For Verstappen \n "
             f"Pre-season Bahrain vs 2021 Race Bahrain")

plt.show()

