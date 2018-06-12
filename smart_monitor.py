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
#import os
#pdb.set_trace()

class SmartSwitch(simple_switch_stp_13.SimpleSwitch13):

    def __init__(self, *args, **kwargs):
        """
            Constructor for the SmartSwitch
            datapaths: The devices connected to the controller. 
        """
        super(SmartSwitch, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)
        self._temp_bandwidth_bytes = 0
        self.num_links = 0
        self.port_wise_bandwidth = {}
        self.prev_bandwidth = 0
        self.port_speed = {}
        self.port_features = {}
        self.port_stats = {}
        self.congestion_score = {}
        self.state_len = 3
        self.sleep_period = 10
        self.switch_analyzers = {}
        self.switch_statistics = {}
        # self.bandwidth_agent = Agent([10, 20, 100], 100, 1)
        # self.bandwidth_agent.initialize_model(0)
        # self.decision_agent = Agent([10, 20, 2], 2, 1)
        # self.decision_agent.initialize_model(0)
        self.switch_analyzers = {}
        self.switch_stats = {}


    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        """
            A handler function for OFP Event State change on the controller. 
            @params: 
                ev: The OFP Event Object. 

        """
        datapath = ev.datapath

        if ev.state == MAIN_DISPATCHER: 
            self.logger.debug('register datapath: %016x', datapath.id)
            self.datapaths[datapath.id] = datapath
            #self.switch_analyzers[datapath.id] = Analyzer("s{}-eth1".format(int(datapath.id)))
            #threading.Thread(target=self.switch_analyzers[datapath.id].start_running).start()
            #self.switch_analyzers[datapath.id].start_running()
            #self.switch_statistics[datapath.id] = {}
        elif ev.state == DEAD_DISPATCHER: 
            self.logger.debug('unregister datapath: %016x', datapath.id)
            del self.datapaths[datapath.id]
            #del self.switch_analyzers[datapath.id]
            #del self.switch_statistics[datapath.id]
    
    def _monitor(self):
        #self.logger.info("Testing the bandwidth module")
        #my_temp = BandwidthResponse(0000000000000001, "tcp:127.0.0.1:6632")
        #my_temp.set_bandwidth("s1-eth1", "10000") 
        #print "Inside Monitor"
        #if self.switch_analyzers:
        #    print self.switch_analyzers
        #for i in range(0,5):
        score1= score2=score3=score4=score5=score6=score7=score8=score9=score10=score11=score12 = 0
        File = open("Path.txt",'r')
        path = list(File.read())
        File.close()
        path = path[::-1]
        i=0
        while i<len(path):
            if path[i] == ' ' or path[i] == ',' or path[i] == ']' or path[i] == '[':
                del path[i]
            else:
                i+=1
        for i in range(len(path)):
            path[i] = int(path[i])
            
        while True:
            for dp in self.datapaths.values(): 
                self.port_features.setdefault(dp.id, {})
                self.congestion_score.setdefault(dp.id, {})
               # print self.switch_analyzers[dp.id]
                self._request_stats(dp)
                #print self.switch_analyzers[dp.id]
                #self.switch_statistics[dp.id] = self.switch_analyzers[dp.id].get_statistics

            hub.sleep(self.sleep_period)
            #print "Printing switch statistics:{}".format(self.switch_statistics)
            scores=self._calculate_congestion_score(self.get_network_latency('127.0.0.1'))
            print "latency is : {}".format(self.get_network_latency('127.0.0.1'))
            print "scores are: "
            # if scores == None or len(scores)<7:
            #     print "Scores are being calculated"
            # elif len(scores) >= 8:
            print scores
            csv_cols = ['original', 'connected', 'weight']
    # scores = { 1: {1: 0.987, 2: 0.087, 3: 0.123},
    #            2: {1: 0.087, 2: 0.00088},
    #            3: {1: 0.000885, 2: 0.0088},
    #            4: {1:, 2: cs},
    #            5: {1: cs, 2: cs2, 3: cs3}}
            # dict_data = []
            
            if scores != None:
                # if scores[1][2] > score1:
                #     score1 = scores[1][2]
                # if scores[2][2] > score1:
                #     score2 = scores[2][2]
                # if scores[1][3] > score3:
                #     score3 = scores[1][3]
                # if scores[2][3] > score4:
                #     score4 = scores[2][3]
                # if scores[3][2] > score5:
                #     score5 = scores[3][2]
                # if scores[4][2] > score6:
                #     score6 = scores[4][2]
                # if scores[5][3] > score7:
                #     score7 = scores[5][3]
                # if scores[4][3] > score8:
                #     score8 = scores[4][3]
                # if scores[7][2] > score9:
                #     score9 = scores[7][2]
                # if scores[5][4] > score10:
                #     score10 = scores[5][4]
                # if scores[8][3] > score11:
                #     score11 = scores[8][3]
                # if scores[6][3] > score12:
                #     score12 = scores[6][3]
                
                dict_data = [
                    {'original' : 1, 'connected' : 2, 'weight' : scores[1][2]},
                    {'original' : 2, 'connected' : 3, 'weight' : scores[2][2]},
                    {'original' : 1, 'connected' : 4, 'weight' : scores[1][3]},
                    {'original' : 2, 'connected' : 5, 'weight' : scores[2][3]},
                    {'original' : 3, 'connected' : 6, 'weight' : scores[3][2]},
                    {'original' : 4, 'connected' : 5, 'weight' : scores[4][2]},
                    {'original' : 5, 'connected' : 6, 'weight' : scores[5][3]},
                    {'original' : 4, 'connected' : 7, 'weight' : scores[4][3]},
                    {'original' : 7, 'connected' : 8, 'weight' : scores[7][2]},
                    {'original' : 5, 'connected' : 8, 'weight' : scores[5][4]},
                    {'original' : 8, 'connected' : 9, 'weight' : scores[8][3]},
                    {'original' : 6, 'connected' : 9, 'weight' : scores[6][3]}
                ]
                # self.update_cs(path,packet_nature,data):
                # packetNature = int(self.get_Nature_of_Packet())
                
                # if packetNature == -1:
                print "The path to be avoided {}".format(path)
                for i in range(1,len(path)):
                    for j in range(len(dict_data)):
                        if path[i-1] == dict_data[j]['original'] and path[i] == dict_data[j]['connected']:
                            cs = dict_data[j]['weight']
                            print "Original CS between {} and {} is {}".format(path[i-1],path[i],cs)
                            cs = (cs)*(1 + 0.98)
                            dict_data[j] = {'original' : path[i-1], 'connected' : path[i], 'weight' : cs}
                            print "Enhanced CS with AI is {}".format(dict_data[j])
             # Get the path where the project is stored
                currentPath = os.getcwd()
                    # The file will be stored in /Users/sumitchougule/PycharmProjects/WriteToCSVFile/csv/graph.csv
                csv_file = currentPath + "/graph_cs.csv"
                    # Calling the driver function
                self.writeDictDataToCSVFile(csv_file, csv_cols, dict_data)
                print("write to file")
                
            
            
            '''
            for datapath_ids in self.congestion_score.keys():
                for port_number in self.congestion_score[datapath_ids].keys():
                   
                    suggested_action = self.decision_agent.choose_action(
                            self.congestion_score[datapath_ids][port_number])
                    print "Suggested Action: {}".format(suggested_action)
                    if suggested_action == 0:
                        suggested_bw = self.bandwidth_agent.choose_action(
                                self.congestion_score[datapath_ids][port_number])
                        print "Congestion score[datapath:{}][port:{}] : {}, bw: {}".format(
                                datapath_ids,
                                port_number,
                                self.congestion_score[datapath_ids][port_number],
                                suggested_bw) 
                    elif suggested_action == 1: 
                        print "Congestion score[datapath:{}][port:{}] : {}, flow rule action".format(
                                datapath_ids, 
                                port_number, 
                                self.congestion_score[datapath_ids][port_number])
                                '''

    def _request_stats(self, datapath):
        self.logger.debug('send stats request: %016x', datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        
        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)
         
        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)
       
        #Adding a call to get the port-wise stats for each datapath. For maxrate and bitrate
        req = parser.OFPPortDescStatsRequest(datapath, 0)
        datapath.send_msg(req)


    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
        body = ev.msg.body
        
        #self.logger.info('datapath         port     '
        #                 'rx-pkts  rx-bytes rx-error '
        #                 'tx-pkts  tx-bytes tx-error')
        #self.logger.info('---------------- -------- '
        #                 '-------- -------- -------- '
        #                 '-------- -------- --------')

        #for stat in sorted([flow for flow in body if flow.priority == 1],
        #                    key=lambda flow: (flow.match['in_port'],
        #                    flow.match['eth_dst'])):
                                #self.logger.info('%016x %8x %17s %8x %8d %8d',
                                #                  ev.msg.datapath.id,
                                #                  stat.match['in_port'], stat.match['eth_dst'],
                                #                  stat.instructions[0].actions[0].port,
                                #                  stat.packet_count, stat.byte_count)

        
    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def _port_stats_reply_handler(self, ev):
        body = ev.msg.body
        for stat in sorted(body, key=attrgetter('port_no')):
            if stat.port_no != ofproto_v1_3.OFPP_LOCAL:
                key = (ev.msg.datapath.id, stat.port_no)
                value = (
                    stat.tx_bytes, stat.rx_bytes, stat.rx_errors,
                    stat.duration_sec, stat.duration_nsec)

                self._save_stats(self.port_stats, key, value, self.state_len)

                # Get port speed.
                pre = 0
                period = self.sleep_period
                tmp = self.port_stats[key]
                if len(tmp) > 1:
                    pre = tmp[-2][0] + tmp[-2][1]
                    period = self._get_period(
                        tmp[-1][3], tmp[-1][4],
                        tmp[-2][3], tmp[-2][4])

                speed = self._get_speed(
                    self.port_stats[key][-1][0]+self.port_stats[key][-1][1],
                    pre, period)

                self._save_stats(self.port_speed, key, speed, self.state_len)
    def get_Nature_of_Packet(self):
        # print "Enter Nature of Packet: 0 for Benign, -1 for Malicious"
        return input("Enter Nature of Packet: 0 for Benign, -1 for Malicious: ")
        
        
        
    @set_ev_cls(ofp_event.EventOFPPortDescStatsReply, MAIN_DISPATCHER)
    def port_desc_stats_reply_handler(self, ev):
        """
            Method to handle the portwise description. 
        """
        msg = ev.msg
        dpid = msg.datapath.id
        ofproto = msg.datapath.ofproto

        config_dict = {ofproto.OFPPC_PORT_DOWN: "Down",
                       ofproto.OFPPC_NO_RECV: "No Recv",
                       ofproto.OFPPC_NO_FWD: "No Farward",
                       ofproto.OFPPC_NO_PACKET_IN: "No Packet-in"}

        state_dict = {ofproto.OFPPS_LINK_DOWN: "Down",
                      ofproto.OFPPS_BLOCKED: "Blocked",
                      ofproto.OFPPS_LIVE: "Live"}

        ports = []
        for p in ev.msg.body:
            ports.append('port_no=%d hw_addr=%s name=%s config=0x%08x '
                         'state=0x%08x curr=0x%08x advertised=0x%08x '
                         'supported=0x%08x peer=0x%08x curr_speed=%d '
                         'max_speed=%d' %
                         (p.port_no, p.hw_addr,
                          p.name, p.config,
                          p.state, p.curr, p.advertised,
                          p.supported, p.peer, p.curr_speed,
                          p.max_speed))
            if p.config in config_dict:
                config = config_dict[p.config]
            else:
                config = "up"

            if p.state in state_dict:
                state = state_dict[p.state]
            else:
                state = "up"

            port_feature = (config, state, p.curr_speed)
            if p.port_no != ofproto_v1_3.OFPP_LOCAL:
                self.port_features[dpid][p.port_no] = port_feature

    
    def _save_stats(self, _dict, key, value, length):
        if key not in _dict:
            _dict[key] = []
        _dict[key].append(value)

        if len(_dict[key]) > length:
            _dict[key].pop(0)

    def _get_speed(self, now, pre, period):
        if period:
            return (now - pre) / (period)
        else:
            return 0
    
    def _get_time(self, sec, nsec):
        return sec + nsec / (10 ** 9)

    def _get_period(self, n_sec, n_nsec, p_sec, p_nsec):
        return self._get_time(n_sec, n_nsec) - self._get_time(p_sec, p_nsec)
    
    def _calculate_bandwidth(self, current_val, time_period=5):
        prev_value = self.prev_bandwidth
        self.prev_bandwidth = current_val
        return float(current_val - prev_value) / time_period

    @set_ev_cls(event.EventSwitchEnter)
    def get_links(self, ev):
        """
            This function gives the number of links connected to a switch. 
            For all the switches connected to the controller.
        """
        #print "Printing ip address: {}".format(ev.switch.dp.address)
        switch_list = get_switch(self, None)
        switches=[switch.dp.id for switch in switch_list]
        links_list = get_link(self, None)
        links=[(link.src.dpid,link.dst.dpid,{'port':link.src.port_no}) for link in links_list]
        host_list = []
        for i in switches: 
            host_list.append(get_host(self, i))
         
        #Number of links between switches.
        self.num_links = len(links)
    
    @set_ev_cls(event.EventHostAdd)
    def inc_links(self, ev):
        self.num_links = self.num_links + 1

    @set_ev_cls(event.EventLinkDelete)
    def dec_links(self, ev):
        self.num_links = self.num_links - 1
        
        
    
    def get_network_latency(self, host):
         size_of_packet = 100
         sum_of_te = 0.0
     
         for i in xrange(0, 10):
             initial_time = datetime.datetime.now()
             response = os.system("ping -c 1 -s " +str(size_of_packet) + " " + host + "| > nul")
             finish_time = datetime.datetime.now()
             sum_of_te += ((finish_time - initial_time).microseconds) 
             return float(str(sum_of_te))/10
                       
    
    def _calculate_congestion_score(self, network_latency):
        """
           Populates the self.congestion_score dictionary with the respective
           congestion scores by dpid and port_no. 
           For e.g.
           self.congestion_score[dpid][port_no] = value.
           The curr_speed is divided by 8 as it's the bitrate and the port_speed is in bytes
        """
        #print self.switch_analyzers
        current_num_links = 2
        #print "==============================================="
        #print self.port_features
        
        if bool(self.port_features) and bool(self.port_speed):
            for dpid in self.port_features.keys():
                for port_no in self.port_features[dpid].keys():
                    a, b = self.port_speed[(dpid, port_no)][-1], (self.port_features[dpid][port_no][2]/8)
                    if a > b: 
                        bw_usage = 100
                    else:
                        bw_usage = (a / b) * 100
                    if (network_latency > (2*current_num_links*1000)):
                        latency_estimate = 100
                    else:
                        latency_estimate = (network_latency - (current_num_links*1000))/(current_num_links*1000)
                    #print bw_usage, latency_estimate. The port speed for some reason stays 10 Mbits/s. 
                    #print("Used bandwidth: {}, Available capacity: {}".format(a,b))
                    congestion_score = bw_usage + ((1/(current_num_links*256))*latency_estimate)
                    if (bw_usage == 0) and congestion_score < 0: 
                        congestion_score = 0

                    self.congestion_score[dpid][port_no] = congestion_score
            
            print "==============================================================="        
            return self.congestion_score
        





#import csv
#import os

    def writeDictDataToCSVFile(self,csv_file, csv_cols, dict_data):
        try:
            with open(csv_file, 'w') as csvfile:
                csvWriter = csv.DictWriter(csvfile, fieldnames=csv_cols)
                csvWriter.writeheader()
                for data in dict_data:
                    csvWriter.writerow(data)
        except IOError as (errno, strerror):
            print("I/O error ({0}): {1}".format(errno, strerror))
        return

'''
def handle_congestion(scores):
    csv_cols = ['Source', 'Destination', 'congestion_score']
    # scores = { 1: {1: 0.987, 2: 0.087, 3: 0.123},
    #            2: {1: 0.087, 2: 0.00088},
    #            3: {1: 0.000885, 2: 0.0088},
    #            4: {1:, 2: cs},
    #            5: {1: cs, 2: cs2, 3: cs3}}
    dict_data = [
        {'Source' : 1, 'Destination' : 2, 'congestion_score' : scores[1][2]},
        {'Source' : 1, 'Destination' : 4, 'congestion_score' : scores[1][3]},
        {'Source' : 2, 'Destination' : 3, 'congestion_score' : scores[2][2]},
        {'Source' : 3, 'Destination' : 5, 'congestion_score' : scores[3][2]},
        {'Source' : 4, 'Destination' : 5, 'congestion_score' : scores[4][2]},
    ]

    # Get the path where the project is stored
    currentPath = os.getcwd()
    # The file will be stored in /Users/sumitchougule/PycharmProjects/WriteToCSVFile/csv/graph.csv
    csv_file = currentPath + "/csv/graph.csv"
    # Calling the driver function
    writeDictDataToCSVFile(csv_file, csv_cols, dict_data)'''