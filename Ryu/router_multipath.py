	# Trabalho final Protocolo de Comunicacao - 2014/1
	# Professor: Luciano Paschoal Gaspary
	#  Controlador para OpenFlow - criacao de multiplos caminhos para trafegos
	#  Funciona com OpenFlow v. 1.3
	# Desenvolvido por:
	#  Gustavo Miotto - 171435 - gustavomiotto@gmail.com
	#  Luis Antonio Leiva Hercules - 176038 - tonyleiva6@gmail.com
	# Porto Alegre, 29 de Junho de 2014
	# ( Esqueleto do codigo baseado no codigo simple_switch_13.py - Ryu Controller
	#  disponivel em:  https://github.com/osrg/ryu/blob/master/ryu/app/simple_switch_13.py )

	from ryu.base import app_manager
	from ryu.controller import (ofp_event, dpset)
	from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, DEAD_DISPATCHER
	from ryu.controller.handler import set_ev_cls
	from ryu.ofproto import ofproto_v1_3, ether
	from ryu.lib.packet import packet
	from ryu.lib.packet import ethernet, ipv4, arp
	import networkx as nx
	import itertools
	import random
	import re

	ARP = arp.arp.__name__
	IPV4 = ipv4.ipv4.__name__
	UINT32_MAX = 0xffffffff

	PATH_SIZE = 6
	MULTIPATH_LEVEL = 3

	##control variable for mininet shutdown


	class RouterMultipath(app_manager.RyuApp):
	    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
	    _CONTEXTS = {
		'dpset': dpset.DPSet
	    }

	    def __init__(self, *args, **kwargs):
		super(RouterMultipath, self).__init__(*args, **kwargs)
		self.mac_to_port = {}
		self.dpset = kwargs['dpset']
		self.dp_dict = {}   #dictionary of datapaths
		self.elist = [] # edges list to the graph
        self.edges_ports = {}   # dictionary that maps switches connections with ports
        self.parse_graph()      # call the function that populates the priors variables
        self.graph = nx.MultiGraph()    # create the graph
        self.graph.add_edges_from(self.elist)   # add edges to the graph
        self.paths_defineds = {}    # function that stores paths created
        self.mininet_gone = False
        

    # Descr: pre-made function that receive switch features events
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install table-miss flow entry (not the default action when no 
        #    match occurs in OpenFlow 1.3)
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

        # flow mod to block ipv6 traffic (annoying and not related to the work)
        match = parser.OFPMatch(eth_type=0x86dd)
        actions = []
        self.add_flow(datapath, ofproto.OFP_DEFAULT_PRIORITY, match, actions)


    # Descr: function that installs flow entry on switch
    # Args: datapath: datapath of the switch to install the entry,
    #       priority: priority of the flow entry,
    #       match: rule to be matched (ipv4=....,)
    #       actions: actions to be made after a match
    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]

        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                match=match, instructions=inst)
        datapath.send_msg(mod)

    # Descr: pre-made function that receives packet_in events
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # populate dp_dict: dictionary of datapaths
        if not self.dp_dict:
            for (_dpid,dp) in self.dpset.get_all():
                self.dp_dict[_dpid] = dp
                self.logger.debug("switch id: %s",_dpid)
        
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        reg = re.compile(".([0-9]+)$")

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        ip = pkt.get_protocol(ipv4.ipv4)
        p_arp = pkt.get_protocol(arp.arp)

        header_list = dict((p.protocol_name, p)
                        for p in pkt.protocols if type(p) != str)

        ipv4_src = ip.src if ip != None else p_arp.src_ip
        ipv4_dst = ip.dst if ip != None else p_arp.dst_ip

        dst = eth.dst
        src = eth.src

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})
        
        if ARP in header_list:
            self.logger.info("ARP packet in s%s, src: %s, dst: %s, in_port: %s", dpid, src, dst, in_port)
        else:
            self.logger.info("packet in s%s, src: %s, dst: %s, in_port: %s", dpid, ipv4_src, ipv4_dst, in_port)

        # ipv4 addresses
        src_id = reg.search(ipv4_src).group(1)
        dst_id = reg.search(ipv4_dst).group(1)
        src_host = "h"+src_id
        dst_host = "h"+dst_id
        #defining switch paths to install rules
        paths = list(nx.all_simple_paths(self.graph, src_host, dst_host, PATH_SIZE))

        if len(paths) > 0:
            #check to see if already exists a path (rules in switches) between such hosts
            key = ipv4_src+'-'+ipv4_dst
            if key in self.paths_defineds.keys():
                self.logger.info("already created this path")
            else:
                self.logger.info("we must create this path")
                self.paths_defineds[key] = paths
                
                #first we need to check how many paths we have at all minimum cutoff is PATH_SIZE
                path_num = len(paths)
                if path_num > MULTIPATH_LEVEL: # if num of paths is bigger than MULTIPATH_LEVEL slices the array
                    paths = paths[:MULTIPATH_LEVEL]
                self.logger.info("we have: %s path(s)",path_num)
                self.logger.info("Using %s paths: ", len(paths))
                for path in paths:
                    self.logger.info("\t%s", path)
                group_dict = self.get_group_routers(paths)

                #print (mod_group_entry(paths))
                self.create_route(paths, group_dict)

            # create mac host to send arp reply
            mac_host_dst = "00:04:00:00:00:0"+dst_id if len(dst_id) == 1 else "00:04:00:00:00:"+dst_id
            
            #check to see if it is an ARP message, so if it is send a reply
            if ARP in header_list:
                self.send_arp(datapath, arp.ARP_REPLY, mac_host_dst, src, 
                    ipv4_dst, ipv4_src, src, ofproto.OFPP_CONTROLLER, in_port)
            else:   # if it is not ARP outputs the message to the corresponding port
                #print self.edges_ports
                out_port = self.edges_ports[paths[0][1]][paths[0][2]]
                actions = [parser.OFPActionOutput(out_port)]
                data = None
                if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                    data = msg.data
                out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                          in_port=in_port, actions=actions, data=data)
                datapath.send_msg(out)
        else:
            self.logger.info("Destination unreacheable")

    # Descr:function that creates the buckets for the select_group and install the group_entry
    # Args: group_dict: dictionary of switche to have group entries; group_id: id of the group
    #       dp: datapath of the switch to have the group entry installed
    def set_group_entry (self, group_dict, group_id, dp):#, cmd):
        num_paths = len(group_dict[1])
        self.logger.debug("group_dict: %s, num_paths: %s", group_dict, num_paths)
        weight = 100/num_paths
        self.logger.info("weight is: %s", weight)

        group_router = group_dict[0] 
        self.logger.info("group mod in: %s",group_router)
        buckets = []
        for output in group_dict[1]:
            watch_port = dp.ofproto.OFPP_ANY
            watch_group = dp.ofproto.OFPG_ANY
            out_port = group_dict[1][output]
            action = [dp.ofproto_parser.OFPActionOutput(out_port)]
            buckets.append(dp.ofproto_parser.OFPBucket(
                weight, watch_port, watch_group, action))
        group_mod = dp.ofproto_parser.OFPGroupMod(
            dp, dp.ofproto.OFPGC_ADD, dp.ofproto.OFPGT_SELECT, group_id, buckets)
        dp.send_msg(group_mod)

    # Descr: finds all switches in paths that splits in diff ways (to create multipath) -> group_router
    # Args: paths: array of path
    # Return: group_dict: dictionary of group routers and out ports (of the switches in diff ways)
    def get_group_routers(self, paths):
        path = paths[:]
        group_dict = {}
        #first remove the last router and hosts from the paths
        for i in xrange(0, len(path)):
            path[i] = path[i][1:]
            path[i] = path[i][:-2]

        #intersection of all paths
        intersected_routers = list(set(path[0]).intersection(*path))

        #removing routers already added
        for i in xrange(0, len(path)):
            path[i] = list(set(path[i]) - set(intersected_routers))
        #intersected_routers = []
        
        #intersecting path lists combinations
        rg = range(0,len(path))
        for L in range(2,len(rg)):
            for subset in itertools.combinations(rg,L):
                subpaths = []
                #print subset
                for i in subset:
                    subpaths.append(path[i]) 
                subrouter = list(set(subpaths[0]).intersection(*subpaths))
                intersected_routers.extend(subrouter) if subrouter else None
        #print intersected_routers
        for router in intersected_routers:
            group_router =  router
            #print group_router
            group_dict.setdefault(group_router, {})
            for p in paths:
                if group_router not in p:
                    continue
                out_port = self.edges_ports[group_router][p[p.index(group_router)+1]]
                group_dict[group_router][p[p.index(group_router)+1]] = out_port

        for key in group_dict.keys():
            if len(group_dict[key]) == 1:
                del group_dict[key]
        self.logger.info("group_dict: %s",group_dict)

        return group_dict


    # Descr: install flow entries in the switches received in paths, and group entries in switches in group_dict
    # Args: paths: array of path, group_dict: switches with group entries to be installed
    def create_route(self, paths, group_dict):
        random.seed()
        flow_id = random.randrange(100) # random value to store the group_id
        gid = random.randrange(30) #random value to create the group_id
        #group_id = {dpid: {flow_id: gid}}
        group_id = {}
        # when a switch must have group we need to call set_group_entry:
        for _dict,i in zip(group_dict.iteritems(), xrange(1, len(group_dict)+1)):
            self.set_group_entry(_dict, i+gid, self.dp_dict[int(_dict[0][1:])]) ##group_dict entry, id, datapath from that switch
            group_id.setdefault(_dict[0],{}) if _dict[0] not in group_id.keys() else None
            group_id[_dict[0]][flow_id] = i+gid
        
        #for each router in path we need to install flows
        for path in paths:
            for p,i in zip(path,xrange(0,len(path))):
                if i == 0:
                    continue
                if i == len(path)-1:
                    break
                self.logger.debug("p is: %s",p)
                datapath = self.dp_dict[int(p[1:])]
                parser = datapath.ofproto_parser
                ofproto = datapath.ofproto
                actions = []

                
                if p in group_dict.keys():  # if switch has group_entry his flow entry outputs to group
                    out_port = group_id[p][flow_id]
                    self.logger.info("switch %s -> out to group_id: %s",p,out_port)
                    actions = [parser.OFPActionGroup(out_port)]
                else: # flow entry outputs to a port -> another switch
                    out_port = self.edges_ports[p][path[i+1]]
                    actions = [parser.OFPActionOutput(out_port)]
                    self.logger.info("switch %s -> out_port: %s",p, out_port)
                #here we need to call add_flow the switchs 
                # with output port and ip_src and ip_dst as matches
                ###########################################################################################################
                ip_src = "10.0.0."+path[0][1:]
                ip_dst = "10.0.0."+path[-1][1:]
                match = parser.OFPMatch(eth_type= 0x0800, ipv4_src=ip_src, ipv4_dst=ip_dst) 
                self.add_flow(datapath, ofproto.OFP_DEFAULT_PRIORITY, match, actions)
        
    # Descr: Function that parser the topology.txt file and turns it into a graph
    # Args: None
    def parse_graph(self):
        file = open('topology.txt','r')
        reg = re.compile('-eth([0-9]+):([\w]+)-eth[0-9]+')
        regSwitch = re.compile('(s[0-9]+) lo')

        for line in file:
            if "lo:" not in line:
                continue
            refnode = (regSwitch.match(line)).group(1)
            connections = line[8:]
            self.edges_ports.setdefault(refnode, {})
            for conn in reg.findall(connections):
                self.edges_ports[refnode][conn[1]] = int(conn[0])
                self.elist.append((refnode, conn[1])) if (conn[1], refnode) not in self.elist else None

    # Descr: Function that create and sends arp message
    # Args: datapath: datapath of the switch,
    #       arp_opcode: ARP_TYPE
    #       src_mac, dst_mac: ethernet addresses
    #       src_ip, dst_ip: ipv4 addresses      
    #       arp_target_mac: ethernet addr to be the answer in arp reply
    #       in_port: port were entered the packet, output: out_port to send the packet  
    def send_arp(self, datapath, arp_opcode, src_mac, dst_mac,
                 src_ip, dst_ip, arp_target_mac, in_port, output):
        # Generate ARP packet
        ether_proto = ether.ETH_TYPE_ARP
        hwtype = 1
        arp_proto = ether.ETH_TYPE_IP
        hlen = 6
        plen = 4

        pkt = packet.Packet()
        e = ethernet.ethernet(dst_mac, src_mac, ether_proto)
        a = arp.arp(hwtype, arp_proto, hlen, plen, arp_opcode,
                    src_mac, src_ip, arp_target_mac, dst_ip)
        pkt.add_protocol(e)
        pkt.add_protocol(a)
        pkt.serialize()

        actions = [datapath.ofproto_parser.OFPActionOutput(output)]

        datapath.send_packet_out(in_port=in_port, actions = actions, data=pkt.data)  

    # Descr: Receives port change notification (link up or down in mininet), caused by an event trigger
    # Args: ev (Function pre-made, follows the pattern of the controller OS) 
    @set_ev_cls(ofp_event.EventOFPPortStatus, MAIN_DISPATCHER)
    def port_status_handler(self, ev):
        msg = ev.msg
        dp = msg.datapath
        ofp = dp.ofproto
        switch = "s"+str(dp.id)
        port = msg.desc.name.split('-')[1][3:]

        # search for the switch linked to the port changed
        for key,val in self.edges_ports[switch].iteritems():
            if val == int(port):
                other_switch = key

        self.logger.debug("msg.desc: %s",msg.desc)
        if msg.reason == ofp.OFPPR_MODIFY and self.mininet_gone == False:
            if msg.desc.config == 1: # link down - so remove link in the graph and update flow entries in switch
                self.logger.info("Link Down in dpid: %s port %s with switch %s", switch, port, other_switch)
                if self.graph.has_edge(switch,other_switch):
                    self.graph.remove_edge(switch,other_switch)
                    self.update_flow_entries(switch, 'down')
            elif msg.desc.config == 0: # link up - so add link to the graph and update flow entries in switch
                self.logger.info("Link up in dpid: %s port %s with switch %s", switch, port, other_switch)
                if not self.graph.has_edge(switch, other_switch):
                    self.graph.add_edge(switch, other_switch)
                    self.update_flow_entries(switch, 'up')
        elif self.mininet_gone:
            self.paths_defineds = {} # as mininet gone all the flows in switches gone together
            self.dp_dict = {}
        
    # Desc: Clear flow entries of the switches belonging to the path that the reiceved switch was
    # Args: switch were the link change occurred
    def update_flow_entries(self, switch, _type):
        if _type == "down" :
            paths_to_remove = []
            for key, value in self.paths_defineds.iteritems():
                self.logger.debug("switches %s, value %s", switch, value)
                val = list(set(value[0]).union(*value))
                if switch in val:
                    paths_to_remove.append(key)
            self.logger.debug("paths to be removed: %s", paths_to_remove)
            switches_to_clear = []
            for a in paths_to_remove:
                paths = self.paths_defineds.get(a)
                switches_to_clear.append(list(set(paths[0]).union(*paths)))
                del self.paths_defineds[a]
            if switches_to_clear:
                switches_to_clear = list(set(switches_to_clear[0]).union(*switches_to_clear))
                switches_to_clear = [elem for elem in switches_to_clear if 'h' not in elem]
                for switch in switches_to_clear:
                    datapath = self.dp_dict[int(switch[1:])]
                    parser = datapath.ofproto_parser
                    match = parser.OFPMatch(eth_type=0x0800)
                    mod = parser.OFPFlowMod(datapath=datapath, 
                                            command=datapath.ofproto.OFPFC_DELETE,
                                            out_port = datapath.ofproto.OFPP_ANY,
                                            out_group= datapath.ofproto.OFPP_ANY,
                                            match=match)
                    datapath.send_msg(mod)
                    self.del_groups(datapath)
        else:
            #if _type is up we have to delete all flow, because we have to create everything again
            # to guarantee that we will cover new possibilities of paths
            self.paths_defineds = {}
            for datapath in self.dp_dict.values():
                #datapath = self.dp_dict[int(switch[1:])]
                parser = datapath.ofproto_parser
                match = parser.OFPMatch(eth_type=0x0800)
                mod = parser.OFPFlowMod(datapath=datapath, 
                                        command=datapath.ofproto.OFPFC_DELETE,
                                        out_port = datapath.ofproto.OFPP_ANY,
                                        out_group= datapath.ofproto.OFPP_ANY,
                                        match=match)
                datapath.send_msg(mod)
                self.del_groups(datapath)

    # Descr: Clear the group table in the switch
    # Args: datapath of the switch to be cleared
    def del_groups(self,dp):
        ofp = dp.ofproto
        parser = dp.ofproto_parser
        mod = parser.OFPGroupMod(dp,
                                 command=ofp.OFPGC_DELETE,
                                 type_=0,
                                 group_id=ofp.OFPG_ALL)
        return dp.send_msg(mod)

    # Descr: Pre-made function that receive State Change notifications, used to
    #        realize when the mininet was closed
    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def state_change_handler(self, ev):
        if ev.state == DEAD_DISPATCHER:
            self.logger.debug("Mininet was shutdown")
            self.mininet_gone = True
        elif ev.state == MAIN_DISPATCHER:
            self.mininet_gone = False
