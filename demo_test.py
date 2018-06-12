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
# //////////////////////////////////////////////////////////////////////////// 

class ExampleShortestForwarding(app_manager.RyuApp):
	
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(ExampleShortestForwarding, self).__init__(*args, **kwargs)
        self.network=nx.DiGraph()
        self.topology_api_app = self
        self.paths = {}
		
		
	
	@set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
	def switch_features_handler(self, ev):
		datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        ofp_parser = datapath.ofproto_parser

        # install the table-miss flow entry.
        match = ofp_parser.OFPMatch()
        actions = [ofp_parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        ofp_parser = datapath.ofproto_parser

        # construct flow_mod message and send it.
        inst = [ofp_parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                            actions)]
        mod = ofp_parser.OFPFlowMod(datapath=datapath, priority=priority,
                               match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(event.EventSwitchEnter, [CONFIG_DISPATCHER, MAIN_DISPATCHER])
    def get_topology(self, ev):
        # get switches and store them into self.network
        switch_list = get_switch(self.topology_api_app, None)   
        switches=[switch.dp.id for switch in switch_list]
        self.network.add_nodes_from(switches)
    
        # get links and store them into self.network
        links_list = get_link(self.topology_api_app, None)
        links=[(link.src.dpid,link.dst.dpid,{'port':link.src.port_no}) for link in links_list]
        self.network.add_edges_from(links)

        # reverse link.
        links=[(link.dst.dpid,link.src.dpid,{'port':link.dst.port_no}) for link in links_list]
        self.network.add_edges_from(links)

    def get_out_port(self, src, dst, datapath, in_port):
        dpid = datapath.id
        # add link between host and ingress switch.
        if src not in self.network:
            self.network.add_node(src)
            self.network.add_edge(dpid,src,{'port':in_port})
            self.network.add_edge(src,dpid)
            self.paths.setdefault(src, {})

        if dst in self.network:
            # if path is not existed, calculate it and save it.
            if dst not in self.paths[src]:
                path = nx.shortest_path(self.network,src,dst)
				src_id = path[1]   #9 or 1
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
				for i in range(len(shortest)):
					path_ql.append(shortest[i])
				# path.append(shortest)				#['src',shortest,'dst']
				# path.append(dst)
				path_ql.append(dest_temp)		#['00:00:00:00:00:02', 1, 4, 9, '00:00:00:00:00:01']
				self.paths[src][dst] = path_ql		
				# path.insert(0,src)
				print('The optimal path is: {}'.format(path_ql))
				next = path_ql[path_ql.index(dpid)+1]
				out_port = self.network[dpid][next]['port']
				
				
				
				
				

            # find out_port to next hop.
            #path = self.paths[src][dst]
            #print "path: ", path
            #next_hop = path[path.index(dpid)+1]
            #out_port = self.network[dpid][next_hop]['port']
        else:
            out_port = datapath.ofproto.OFPP_FLOOD

        return out_port

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        ofp_parser = datapath.ofproto_parser

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        in_port = msg.match['in_port']

        out_port = self.get_out_port(eth.src, eth.dst, datapath, in_port)
        actions = [ofp_parser.OFPActionOutput(out_port)]
        # install flow_mod to avoid packet_in next time.
        if out_port != ofproto.OFPP_FLOOD:
            match = ofp_parser.OFPMatch(in_port=in_port, eth_dst=eth.dst)
            self.add_flow(datapath, 1, match, actions)

        # send packet_out msg to flood packet.
        out = ofp_parser.OFPPacketOut(
            datapath=datapath,buffer_id=msg.buffer_id,in_port=in_port,
            actions=actions)
        datapath.send_msg(out)
###########################################################################################
    
	
	
	
################################################################################################# 
