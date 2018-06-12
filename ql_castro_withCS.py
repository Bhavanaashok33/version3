"""
An OpenFlow 1.0 shortest path forwarding implementation.
"""

import logging
import struct

from ryu.base import app_manager
from ryu.controller import mac_to_port
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0
from ryu.lib.mac import haddr_to_bin
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet

from ryu.topology.api import get_switch, get_link
from ryu.app.wsgi import ControllerBase
from ryu.topology import event, switches
import networkx as nx
# from QL_CODE_testing.main import qcode
# Dependencies for QLCODE/////////////////////////////////////////////////// 
# from getAdjacencyList import getAdjacencyList
# from get_R_Q_matrices import get_initial_R_matrix
# from get_R_Q_matrices import get_initial_Q_matrix
# from getResult import getResult
# from qlcode import qlcode
from qlcode import qlcode
import pandas as pd
import csv
# //////////////////////////////////////////////////////////////////////////// 

class ProjectController(app_manager.RyuApp):
	
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(ProjectController, self).__init__(*args, **kwargs)
		# super(QL, self).__init__(*args)
        self.mac_to_port = {}
        self.topology_api_app = self
        self.net=nx.DiGraph()
        self.nodes = {}
        self.links = {}
        self.no_of_nodes = 0
        self.no_of_links = 0
        self.i=0
		


    # Handy function that lists all attributes in the given object
    def ls(self,obj):
        print("\n".join([x for x in dir(obj) if x[0] != "_"]))
	
    def add_flow(self, datapath, in_port, dst, actions):
        ofproto = datapath.ofproto

        match = datapath.ofproto_parser.OFPMatch(
            in_port=in_port, dl_dst=haddr_to_bin(dst))

        mod = datapath.ofproto_parser.OFPFlowMod(
            datapath=datapath, match=match, cookie=0,
            command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
            priority=ofproto.OFP_DEFAULT_PRIORITY,
            flags=ofproto.OFPFF_SEND_FLOW_REM, actions=actions)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
		# = ev.msg.switch.dp.id
		# print msg
        datapath = msg.datapath
		# dpathid = datapath.dpid
		
        ofproto = datapath.ofproto

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
		
        dst = eth.dst
        src = eth.src
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})
        #print "nodes"
        #print self.net.nodes()
        #print "edges"
        #print self.net.edges()
        #self.logger.info("packet in %s %s %s %s", dpid, src, dst, msg.in_port)
        if src not in self.net:
            self.net.add_node(src)
            self.net.add_edge(dpid,src,{'port':msg.in_port})
            self.net.add_edge(src,dpid)
        if dst in self.net:
			
			# data = example()
			
			# switch_ids=self.get_topology_data(ev)
			# print('The switches are: {}'.format(switch_ids))
			#######HANDLE AMIT'S CODE$###################
			# src_id = eth.dpid
			# dst_id = eth.dpid
			path=nx.shortest_path(self.net,src,dst)
			#calculate src_id and dst_id
			src_id = path[1]		#9 or 1
			dst_id = path[len(path)-2]		#1 or 9
			src_temp = path[0]			# ::02 or ::01
			dest_temp = path[len(path)-1]		# ::01 or ::02
			data = pd.read_csv("graph_cs.csv")
			result = qlcode(data,src_id,dst_id)		#pass src and dest dpids as parameters
			# print result
			des = result["ends_find"]		#[1] or [9]
			path_ql=[]
			# path.append(src)
			path_ql.append(src_temp)
			shortest = result["all_routes"][des[0]][0]	    #[9,4,1] or [1,4,9]
			# self.writePathToCSVFile("Path.csv", shortest)
			if shortest:
				File = open('Path.txt','w')
				File.write(str(shortest))
				File.close()
			for i in range(len(shortest)):
				path_ql.append(shortest[i])
			# path.append(shortest)				#['src',shortest,'dst']
			# path.append(dst)
			path_ql.append(dest_temp)		#['00:00:00:00:00:02', 1, 4, 9, '00:00:00:00:00:01']

			# path.insert(0,src)
			print('The optimal path is: {}'.format(path_ql))
			
			next = path_ql[path_ql.index(dpid)+1]
			out_port = self.net[dpid][next]['port']
			# print('Path: {}'.format(path))
			
			###################################nx. Shortest path code in-built function//////// 
            #print (src in self.net)
            # print nx.shortest_path(self.net,1,4)
            #print nx.shortest_path(self.net,4,1)
            # print nx.shortest_path(self.net,src,4)

            # path=nx.shortest_path(self.net,src,dst)
# 			CALL AMITS CODE HERE/////////////////////////////////////////////////////////////////////////////////////////////////////////
			
			
			# main
			# data = pd.read_csv("graph.csv")
			# graph = getAdjacencyList(data)
			# 
			# A = graph["A"]
			# Z = graph["Z"]
			# weight = graph["weight"]
			# A_Z_dict = graph["A_Z_dict"]
			# 
			# src = 1
			# dest = [9]
			# R = get_initial_R_matrix(A, Z, weight, A_Z_dict)
			# Q = get_initial_Q_matrix(R)
			# 
			# alpha = 0.7 # learning rate
			# epsilon = 0.1 # greedy policy
			# n_episodes = 1000 # no of episodes
			# 
			# result = getResult(R, Q, alpha, epsilon, n_episodes, src, dest)
			# Destination = result["ends_find"][0]
			# print("Destination =", result["ends_find"])
			# for key, value in result["cost"].items():
			# 	print("Total cost =", key)
			# 	print("No of paths with cost {} = {}".format(key,value))
			# #print(result["routes_number"])
			# print("Paths =",result["all_routes"])
			# 
			
			
			# print('result is {}'.format(result))
			####NEW MODIFCATIONS ACC TO LOGIC####
			# paths=result["all_routes"]
			# shortest=paths[Destination][0]
			# print(shortest)


################################################################################################# 

			# path=result["all_routes"]
            # print "Path: {}".format(path)
# 			next = path[path.index(dpid)+1]
#             # print "Next: {}".format(next)
# 			out_port = self.net[dpid][next]['port']
            
            # print "Outport: {}".format(out_port)    
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            self.add_flow(datapath, msg.in_port, dst, actions)

        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath, buffer_id=msg.buffer_id, in_port=msg.in_port,
            actions=actions)
        datapath.send_msg(out)
		
#     def writePathToCSVFile(self, csv_file, path):
# 		try:
# 			with open(csv_file, 'w') as csvfile:
# 				# csvWriter = csv.DictWriter(csvfile, fieldnames=csv_cols)
# 				# csvWriter.writeheader()
# 				# for data in dict_data:
# 				csvWriter.writerow(path)
# 		except IOError as (errno, strerror):
# 			print("I/O error ({0}): {1}".format(errno, strerror))
# 		return
	
    @set_ev_cls(event.EventSwitchEnter)
    def get_topology_data(self, ev):		#Work on extracting switches of the hosts
        switch_list = get_switch(self.topology_api_app, None)   
        switches=[switch.dp.id for switch in switch_list]
        self.net.add_nodes_from(switches)
        
        #print "**********List of switches"
        #for switch in switch_list:
        #self.ls(switch)
        #print switch
        #self.nodes[self.no_of_nodes] = switch
        #self.no_of_nodes += 1
	
        links_list = get_link(self.topology_api_app, None)
        #print links_list
        links=[(link.src.dpid,link.dst.dpid,{'port':link.src.port_no}) for link in links_list]
        #print links
		
        self.net.add_edges_from(links)
        links=[(link.dst.dpid,link.src.dpid,{'port':link.dst.port_no}) for link in links_list]
        #print links
		# return links
        self.net.add_edges_from(links)
        
        # print "**********List of links"
        # print self.net.edges()
        #for link in links_list:
	    #print link.dst
            #print link.src
            #print "Novo link"
	    #self.no_of_links += 1
      
        
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	#print "@@@@@@@@@@@@@@@@@Printing both arrays@@@@@@@@@@@@@@@"
    #for node in self.nodes:	
	#    print self.nodes[node]
	#for link in self.links:
	#    print self.links[link]
	#print self.no_of_nodes
	#print self.no_of_links

    #@set_ev_cls(event.EventLinkAdd)
    #def get_links(self, ev):
	#print "################Something##############"
	#print ev.link.src, ev.link.dst
