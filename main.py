from __future__ import absolute_import
from __future__ import print_function

import os
import sys

from filegenerator import *
from utils import *

# The environment variable SUMO_HOME must be set before running the script.
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # Ignore IDE warning
import traci  # Ignore IDE warning

ori_file_path = 'data/'

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

'''
<tlLogic id="J1" type="static" programID="0" offset="0">
        <phase duration="40" state="GGrGG"/> 0
        <phase duration="3"  state="GGrGY"/> 1
        <phase duration="15" state="GGgGr"/> 2
        <phase duration="3"  state="GGyGr"/> 3
</tlLogic>
'''


def writefile():
    a = generate_routefile(path=ori_file_path, demand=demand, time=running_time)
    b, c = generate_addnetfile(path=ori_file_path, distance=detector_loc, isMajor=isMajor)
    d = generate_sumocfgfile(path=ori_file_path, time=running_time, step_length=SIM_INTERVAL)
    return a, b, c, d


# detector is set on the minor_road
def minor_road(gui, phase_parameter: list):
    # store time
    green_duration = 0.0
    interval_duration = 0.0
    clock = 0.0

    # initialize the first phase
    traci.trafficlight.setPhase("J1", 0)
    gui.get_update(0)

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        clock = float(traci.simulation.getTime())  # return current time (in seconds)
        if clock % 10 == 0:
            print('current time: {}, green_duration: {}, interval_duration: {}'.format(clock, green_duration,
                                                                                       interval_duration))
        if traci.trafficlight.getPhase("J1") == 0:
            if traci.inductionloop.getLastStepVehicleNumber("CarDetector") > 0:
                # set yellow light to help change phase
                gui.get_update(1)
                print('Detectors is triggered! minor road green!')
                traci.trafficlight.setPhase("J1", 1)
                gui.get_update(2)
                green_duration = clock + phase_parameter[1]
                interval_duration = green_duration + MAX_GREEN_TIME_MINOR
            else:
                traci.trafficlight.setPhase("J1", 0)
        elif traci.trafficlight.getPhase("J1") == 2:
            if clock - green_duration <= MIN_GREEN_TIME_MINOR:
                pass
            else:
                if (traci.inductionloop.getLastStepVehicleNumber("CarDetector") > 0) and (clock - green_duration <=
                                                                                          MAX_GREEN_TIME_MINOR):
                    gui.get_update(3)
                    print('Detectors is triggered!')
                    gui.get_update(2)
                    interval_duration = clock
                elif (clock - interval_duration <= TIME_UNIT) and (clock - green_duration <= MAX_GREEN_TIME_MINOR):
                    pass
                else:
                    gui.get_update(4)
                    print('main road green! minor road green duration: {}'.format(clock - green_duration))
                    traci.trafficlight.setPhase("J1", 3)
                    gui.get_update(0)
                    continue

        else:
            pass


# detector is set on the major_road
def major_road(gui):
    # store time
    green_duration = 0.0
    phase_signal = True
    phase_signal_minor = True
    interval_duration = 0.0
    clock = 0.0

    # initialize the first phase
    traci.trafficlight.setPhase("J1", 0)
    gui.get_update(0)

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        clock = float(traci.simulation.getTime())  # return current time (in seconds)
        if clock % 10 == 0:
            print('current time: {}, green_duration: {}, interval_duration: {}'.format(clock, green_duration,
                                                                                       interval_duration))
        if (traci.trafficlight.getPhase("J1") == 0) and phase_signal:
            gui.get_update(0)
            print('main road green!')
            green_duration = clock
            interval_duration = green_duration + MIN_GREEN_TIME_MAJOR
            phase_signal = False
        else:
            pass

        if traci.trafficlight.getPhase("J1") == 0:
            if clock - green_duration <= MIN_GREEN_TIME_MAJOR:
                pass
            else:
                gui.get_update(1)
                if ((traci.inductionloop.getLastStepVehicleNumber("CarDetector") > 0) or (
                        traci.inductionloop.getLastStepVehicleNumber("CarDetector_1") > 0)) and (
                        clock - green_duration <= MAX_GREEN_TIME_MAJOR):
                    gui.get_update(2)
                    print('Detectors is triggered!')
                    gui.get_update(0)
                    interval_duration = clock
                elif (clock - interval_duration <= TIME_UNIT) and (clock - green_duration <= MAX_GREEN_TIME_MAJOR):
                    pass
                else:
                    if clock - green_duration > MAX_GREEN_TIME_MAJOR:
                        gui.get_update(5)
                    print('minor road green! main road green duration: {}'.format(clock - green_duration))
                    traci.trafficlight.setPhase("J1", 1)
                    gui.get_update(3)
                    phase_signal = True
                    phase_signal_minor = True
        elif traci.trafficlight.getPhase("J1") == 3 and phase_signal_minor:
            gui.get_update(4)
            phase_signal_minor = False
        else:
            pass


def run():
    a, b, c, d = writefile()

    # open SUMO-GUI for visualization
    sumoBinary = checkBinary('sumo-gui')
    phase_parameter = read_tlLogic("J1")
    traci.start([sumoBinary, "-c", "ASC.sumo.cfg"])
    if traci.gui.hasView(viewID='View #0'):
        traci.gui.setZoom(viewID='View #0', zoom=800.0)
        traci.gui.setOffset(viewID='View #0', x=0.0, y=0.0)
    # flow chart
    gui_thread = GUIThread(isMajor, PAUSE)
    gui_thread.start()
    if isMajor:
        major_road(gui_thread)
    else:
        minor_road(gui_thread, phase_parameter)

    traci.close(wait=False)
    sys.stdout.flush()
    # remove redundant files
    for f in [a, b, c, d]:
        os.remove(f)


if __name__ == "__main__":
    run()
