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
from matplotlib.patches import ConnectionPatch
from numpy import arange, sin, cos

# Enable cache
f1.Cache.enable_cache('cache')

#setup plotting
plotting.setup_mpl(mpl_timedelta_support=True, color_scheme='fastf1', misc_mpl_mods=True)

preseasonb_day3 = f1.get_testing_session(2022, 2, 3)
bahrain_2021 = f1.get_session(2021, 1, 'R')
bahrain_2022 = f1.get_session(2022, 1, 'Q')

lapss = preseasonb_day3.load_laps(with_telemetry=True)
laps = bahrain_2022.load_laps(with_telemetry=True)
#mind, maxd = 0, 5400
mind, maxd = 2300, 3200



# Lec2022 = laps.pick_driver('1').pick_fastest()
# Ham2021 = laps_old.pick_driver('VER').pick_fastest()


Lec_lap = laps.pick_driver('16').pick_fastest()
Ham_lap = laps.pick_driver('44').pick_fastest()
colormap = matplotlib.cm.plasma





# data = pd.DataFrame(ham_laps)
# data.to_excel(r'C:\Users\GAMER\PycharmProjects\f1Project\HamLapBahrain3.xlsx', index = False)
# print(data)

rbr_color = f1.plotting.team_color('RBR')
fer_color = f1.plotting.team_color('FER')
merc_color = f1.plotting.team_color('MER')


fig, ax = plt.subplots(5, sharex='all', squeeze=True)


delta_time, ref_tel, compare_tel = utils.delta_time(Lec_lap, Ham_lap)

Lec_lap = laps.pick_driver('16').pick_fastest().get_car_data().add_distance()
Ham_lap = laps.pick_driver('44').pick_fastest().get_car_data().add_distance()
teste = laps.pick_driver('44').pick_fastest()

# ====================================================

# Ham_lap.loc[Ham_lap['Brake'] > 95, 'CurrentAction'] = 'Brake'
# Ham_lap.loc[(Ham_lap['Throttle'] < 95) & (Ham_lap['Brake'] < 95), 'CurrentAction'] = 'cornering'
# Ham_lap.loc[Ham_lap['Throttle'] > 95, 'CurrentAction'] = 'WOT'
#
#
# Lec_lap.loc[Lec_lap['Brake'] > 95, 'CurrentAction'] = 'Brake'
# Lec_lap.loc[(Lec_lap['Throttle'] < 95) & (Lec_lap['Brake'] < 95), 'CurrentAction'] = 'cornering'
# Lec_lap.loc[Lec_lap['Throttle'] > 95, 'CurrentAction'] = 'WOT'
#
# Ham_lap['ActionID'] = (Ham_lap['CurrentAction'] != Ham_lap['CurrentAction'].shift(1)).cumsum()
# Lec_lap['ActionID'] = (Lec_lap['CurrentAction'] != Lec_lap['CurrentAction'].shift(1)).cumsum()
#
# actions_driver_1 = Ham_lap[['ActionID', 'CurrentAction', 'Distance']].groupby(['ActionID', 'CurrentAction']).max('Distance').reset_index()
# actions_driver_2 = Lec_lap[['ActionID', 'CurrentAction', 'Distance']].groupby(['ActionID', 'CurrentAction']).max('Distance').reset_index()
#
# actions_driver_1['Driver'] = 'HAM'
# actions_driver_2['Driver'] = 'LEC'
#
# actions_driver_1['DistanceDelta'] = actions_driver_1['Distance'] - actions_driver_1['Distance'].shift(1)
# actions_driver_1.loc[0, 'DistanceDelta'] = actions_driver_1.loc[0, 'Distance']
#
# actions_driver_2['DistanceDelta'] = actions_driver_2['Distance'] - actions_driver_2['Distance'].shift(1)
# actions_driver_2.loc[0, 'DistanceDelta'] = actions_driver_2.loc[0, 'Distance']
#
# all_actions = actions_driver_1.append(actions_driver_2)
#
# telemetry_colors = {
#     'WOT': 'green',
#     'cornering': 'yellow',
#     'Brake': 'red',
# }
# for driver in ['HAM', 'LEC']:
#     driver_actions = all_actions.loc[all_actions['Driver'] == driver]
#
#     previous_action_end = 0
#     for _, action in driver_actions.iterrows():
#         ax[1].barh(
#             [driver],
#             action['DistanceDelta'],
#             left=previous_action_end,
#             color=telemetry_colors[action['CurrentAction']]
#         )
#
#         previous_action_end = previous_action_end + action['DistanceDelta']
# ax[1].spines['top'].set_visible(False)
# ax[1].spines['right'].set_visible(False)
# ax[1].spines['left'].set_visible(False)
#
# labels = list(telemetry_colors.keys())
# handles = [plt.Rectangle((0,0),1,1, color=telemetry_colors[label]) for label in labels]
# ax[1].legend(handles, labels)
# ====================================================

ax[1].plot(ref_tel['Distance'], delta_time, '--', color='white')

ax[0].plot(Lec_lap['Distance'], Lec_lap['Speed'], color=fer_color, label='Leclerc')
ax[0].plot(Ham_lap['Distance'], Ham_lap['Speed'], color=merc_color, label='Hamilton')

ax[3].plot(Lec_lap['Distance'], Lec_lap['Brake'], color=fer_color, label='Leclerc')
ax[3].plot(Ham_lap['Distance'], Ham_lap['Brake'], color=merc_color, label='Hamilton')

ax[4].plot(Lec_lap['Distance'], Lec_lap['Throttle'], color=fer_color, label='Leclerc')
ax[4].plot(Ham_lap['Distance'], Ham_lap['Throttle'], color=merc_color, label='Hamilton')

ax[2].plot(Lec_lap['Distance'], Lec_lap['RPM'], color=fer_color, label='Leclerc')
ax[2].plot(Ham_lap['Distance'], Ham_lap['RPM'], color=merc_color, label='Hamilton')

ax[4].set_xlabel('Distance (m)')
ax[0].set_ylabel("Speed (km/h)")
ax[1].set_ylabel("Time delta")
ax[2].set_ylabel("RPM")
ax[3].set_ylabel("Brake")
ax[4].set_ylabel("Throttle")
# ax[0].set_ylabel('Speed in km/h')
fig.align_ylabels(axs=[0, 4])


ax[1].legend()
plt.suptitle(f"Fastest Quali Lap Comparison \n "
             f"2022 Bahrain // Leclerc VS Hamilton")

ax[0].set_xlim(mind, maxd)
ax[1].set_xlim(mind, maxd)
ax[2].set_xlim(mind, maxd)
ax[3].set_xlim(mind, maxd)


# plt.subplot_tool()
plt.tight_layout()
plt.rcParams['figure.figsize'] = [30, 20]
plt.show()

