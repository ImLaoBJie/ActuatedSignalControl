import os
import sys
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element

# The environment variable SUMO_HOME must be set before running the script.
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # Ignore IDE warning
import traci  # Ignore IDE warning


def generate_routefile(path: str, demand: dict, time: int):
    file_path = path + 'ASC.rou.xml'
    tree = ElementTree()
    tree.parse(file_path)
    # get parent
    root = tree.getroot()
    ids = demand.keys()
    for flow in root.iter('flow'):
        id = str(flow.attrib['id'])
        if id not in ids:
            raise Exception('Invalid Demand!')
        else:
            flow.set('probability', str(demand[id]))

    for flow in root.iter('flow'):
        flow.set('end', str(int(time)))

    tree.write('ASC.rou.xml')
    return 'ASC.rou.xml'


def generate_addnetfile(path: str, distance: float, isMajor: bool):
    # Read and copy ASC.net.xml
    file_path = path + 'ASC.net.xml'
    tree = ElementTree()
    tree.parse(file_path)
    # get parent
    root = tree.getroot()

    length = {'E2': 0.0, 'E0': 0.0, 'E4': 0.0}
    ids = list(length.keys())
    ori_ids = list(length.keys())
    for index in range(len(ids)):
        ids[index] = ids[index] + '_0'
    for lane in root.iter('lane'):
        id = lane.attrib['id']
        if id in ids:
            length[ori_ids[ids.index(id)]] = float(lane.attrib['length'])

    tree.write('ASC.net.xml')

    # Modify ASC.add.xml
    for id in length.keys():
        length[id] = length[id] - distance

    file_path = path + 'ASC.add.xml'
    tree = ElementTree()
    tree.parse(file_path)
    # get parent
    root = tree.getroot()

    if isMajor:
        for add in root.iter('additional'):
            new_element = Element('e1Detector')
            add.append(new_element)
            new_element.set('id', 'CarDetector_1')
            new_element.set('lane', 'E4_1')
            new_element.set('pos', str(length['E4']))
            new_element.set('freq', '1.00')
            new_element.set('file', 'CarDetector_1.xml')
            new_element.set('friendlyPos', '1')
            break
        for detector in root.iter('e1Detector'):
            if detector.attrib['id'] == 'CarDetector':
                detector.set('lane', 'E0_0')
                detector.set('pos', str(length['E0']))
                break
    else:
        for detector in root.iter('e1Detector'):
            if detector.attrib['id'] == 'CarDetector':
                detector.set('pos', str(length['E2']))

    tree.write('ASC.add.xml')
    return 'ASC.net.xml', 'ASC.add.xml'


def generate_sumocfgfile(path: str, time: int, step_length: float):
    file_path = path + 'ASC.sumo.cfg'
    tree = ElementTree()
    tree.parse(file_path)
    # get parent
    root = tree.getroot()

    for value in root.iter('end'):
        value.set('value', str(int(time)))

    for value in root.iter('step-length'):
        value.set('value', str(round(step_length, 2)))

    tree.write('ASC.sumo.cfg')
    return 'ASC.sumo.cfg'
