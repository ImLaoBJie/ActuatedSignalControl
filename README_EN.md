# Actuated Signal Control
This simulation of Actuated Signal Control on a intersection is running on the SUMO

### Reference
* <<Traffic Management & Control>>，ISBN：978-7-114-06838-6

### Principle and procedure

Detailed flow chart can be witnessed when running the `main.py`

### TODO
- [x] Simulation of Actuated Signal Control with detector(s) set on main road and minor road respectively.
- [ ] Both roads linked to the single intersection are equipped with a detector.

# Demo

Carton in the demonstration is deliberately done, in order to facilitate the flow chart clear observation, 
if you do not want to meet Carton, you set the variable `PAUSE' in `main.py' to smaller values or even to 0.

![demo](https://raw.githubusercontent.com/ImLaoBJie/ActuatedSignalControl/master/images/demo.gif "demo")

# Quick Start

1.Download the simulation software SUMO（Simulation of Urban Mobility）：[SUMO](http://sumo.sourceforge.net/),

* SUMO is an open source, highly portable, microscopic and continuous traffic simulation package designed to handle 
large road networks. It is mainly developed by employees of the Institute of Transportation Systems at the German Aerospace Center. 
SUMO is open source, licensed under the EPLv2.

2.Install the packages mentioned in `requirements.txt`;

3.Open `main.py` and modify the parameters below:
```
# where the XML files locate
ori_file_path = 'data/'

# the total time of simulation
running_time = 3600

# define the step-length, dont set it at some weird numbers (e.g. 0.33, 0.36, etc.). Otherwise, the SUMO simulator may
# meet some mistakes accidentally.
SIM_INTERVAL = 0.20

# If you want to watch changes of flow chart clearly, set it at high values.
# set it at 0 and no delay.
PAUSE = 0.25

# demand per second from different directions
demand = {'NTOS': 0.2, 'ETON': 0.1, 'ETOS': 0.02, 'STOE': 0.1, 'STON': 0.2}

# If detector is set on the minor_road, isMajor = False
# If detector is set on the major_road, isMajor = True
isMajor = True

# the distance between detector and stop line
if isMajor:
    detector_loc = 30.0
else:
    detector_loc = 3.0  # minimum: 3m

# increment of time
TIME_UNIT = 2.0

# minimum green time for the vehicles
MIN_GREEN_TIME_MINOR = TIME_UNIT
MIN_GREEN_TIME_MAJOR = 30.0 + TIME_UNIT

# The maximum time each phase
MAX_GREEN_TIME_MINOR = 10.0
MAX_GREEN_TIME_MAJOR = 50.0
```

* Initial green time depending on the distance between the detector and the stop line

The distance between the detector and the stop line（m） | Initial green time（s）
------------ | -------------
0～12 | 8
13～18 | 10
19～24 | 12
25～30 | 14
31～36 | 16

4.Run `main.py`。
