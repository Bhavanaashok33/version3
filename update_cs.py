from __future__ import division
from operator import attrgetter
from ryu.app import simple_switch_stp_13           
from ryu.controller import ofp_event
from ryu.controller import conf_switch
from ryu.controller import dpset
from ryu.ofproto import ofproto_v1_3
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub
import time
import datetime
import os
from ryu.topology import event, switches
from ryu.topology.api import get_switch, get_link, get_host
#from ryu.app.ThreatResponse import BandwidthResponse   #error here
#from ryu.app import conf_switch_key as cs_key

#from ryu.intelligence.keras_agent import Agent
#import pdb
#from "../lib/traffic/analyzer" import Analyzer
# from ryu.lib.traffic.analyzer import Analyzer
import threading
import csv

def update_cs(path,packet_nature,data):
    scores=self._calculate_congestion_score(self.get_network_latency('127.0.0.1'))
    csv_cols = ['original', 'connected', 'weight']
# scores = { 1: {1: 0.987, 2: 0.087, 3: 0.123},
#            2: {1: 0.087, 2: 0.00088},
#            3: {1: 0.000885, 2: 0.0088},
#            4: {1:, 2: cs},
#            5: {1: cs, 2: cs2, 3: cs3}}
    # dict_data = []
    
    if scores != None:
        if scores[1][2] > score1:
            score1 = scores[1][2]
        if scores[2][2] > score1:
            score2 = scores[2][2]
        if scores[1][3] > score3:
            score3 = scores[1][3]
        if scores[2][3] > score4:
            score4 = scores[2][3]
        if scores[3][2] > score5:
            score5 = scores[3][2]
        if scores[4][2] > score6:
            score6 = scores[4][2]
        if scores[5][3] > score7:
            score7 = scores[5][3]
        if scores[4][3] > score8:
            score8 = scores[4][3]
        if scores[7][2] > score9:
            score9 = scores[7][2]
        if scores[5][4] > score10:
            score10 = scores[5][4]
        if scores[8][3] > score11:
            score11 = scores[8][3]
        if scores[6][3] > score12:
            score12 = scores[6][3]
        
        dict_data = [
            {'original' : 1, 'connected' : 2, 'weight' : score1},
            {'original' : 2, 'connected' : 3, 'weight' : score2},
            {'original' : 1, 'connected' : 4, 'weight' : score3},
            {'original' : 2, 'connected' : 5, 'weight' : score4},
            {'original' : 3, 'connected' : 6, 'weight' : score5},
            {'original' : 4, 'connected' : 5, 'weight' : score6},
            {'original' : 5, 'connected' : 6, 'weight' : score7},
            {'original' : 4, 'connected' : 7, 'weight' : score8},
            {'original' : 7, 'connected' : 8, 'weight' : score9},
            {'original' : 5, 'connected' : 8, 'weight' : score10},
            {'original' : 8, 'connected' : 9, 'weight' : score11},
            {'original' : 6, 'connected' : 9, 'weight' : score12}
        ]
        for i in range(1,len(path)):
            for data in dict_data:
                if path[i-1] == data.original and path[i] == data.connected:
                    data.weight = data.weight(1 + 0.98)
     # Get the path where the project is stored
        currentPath = os.getcwd()
            # The file will be stored in /Users/sumitchougule/PycharmProjects/WriteToCSVFile/csv/graph.csv
        csv_file = currentPath + "/graph_cs.csv"
            # Calling the driver function
        writeDictDataToCSVFile(csv_file, csv_cols, dict_data)

def writeDictDataToCSVFile(csv_file, csv_cols, dict_data):
    try:
        with open(csv_file, 'w') as csvfile:
            csvWriter = csv.DictWriter(csvfile, fieldnames=csv_cols)
            csvWriter.writeheader()
            for data in dict_data:
                csvWriter.writerow(data)
    except IOError as (errno, strerror):
        print("I/O error ({0}): {1}".format(errno, strerror))
    return    