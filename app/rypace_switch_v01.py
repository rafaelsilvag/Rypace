# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import struct

from ryu.base import app_manager
from ryu.controller import mac_to_port
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib.ip import ipv4_to_bin, ipv4_to_str
from ryu.lib.packet.icmp import icmp
from ryu.ofproto import ofproto_v1_0
from ryu.lib.mac import haddr_to_bin
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ipv4
from ryu.lib.packet import ipv6
from ryu.lib.packet import tcp
from ryu.lib.packet import udp
from ryu.lib.packet import icmp
from ryu.lib import addrconv
# SQLAlchemy
from database.DatabaseSQL import Ips, Blacklists, Controls, ControlsBlacklists, Session, configDB

class RypaceSwitch(app_manager.RyuApp):
    # Definicao da versao do OpenFlow - MK apenas suporta versao 1.0
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    #Metodo construtor
    def __init__(self, *args, **kwargs):
        super(RypaceSwitch, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        
        self.session = Session()
        self.logger.info("=> Connected on host %s on database %s" % (configDB['hostname'], configDB['database']))
        
    def ipv4_text_to_int(self, ip_text):
        if ip_text == 0:
            return ip_text
        assert isinstance(ip_text, str)
        return struct.unpack('!I', addrconv.ipv4.text_to_bin(ip_text))[0]

    def ipv4_int_to_text(ip_int):
        assert isinstance(ip_int, (int, long))
        return addrconv.ipv4.bin_to_text(struct.pack('!I', ip_int))

    # Adicionar regra na tabela  Fluxo.
    def add_flow(self, datapath, in_port, eth, ip_v4, actions):
        ofproto = datapath.ofproto
        idleTimeout = 2
        hardTimeout = 2

        if(ip_v4):
            nw_src = self.ipv4_text_to_int(ip_v4.src)
            nw_dst = self.ipv4_text_to_int(ip_v4.dst)

            match = datapath.ofproto_parser.OFPMatch(
                in_port=in_port,
                dl_type=eth.ethertype,
                dl_src=haddr_to_bin(eth.src),
                dl_dst=haddr_to_bin(eth.dst),
                nw_proto=ip_v4.proto,
                nw_src=nw_src,
                nw_dst=nw_dst,
            )
        else:
            match = datapath.ofproto_parser.OFPMatch(
                in_port=in_port, dl_type=eth.ethertype,
                dl_src=haddr_to_bin(eth.src),
                dl_dst=haddr_to_bin(eth.dst),)

            idleTimeout = 2
            hardTimeout = 2

        mod = datapath.ofproto_parser.OFPFlowMod(
            datapath=datapath, match=match, cookie=0,
            command=ofproto.OFPFC_ADD, idle_timeout=idleTimeout, hard_timeout=hardTimeout,
            priority=ofproto.OFP_DEFAULT_PRIORITY,
            flags=ofproto.OFPFF_SEND_FLOW_REM, actions=actions)

        datapath.send_msg(mod)

    def add_flow_drop(self, datapath, in_port, eth, ip_v4):
        ofproto = datapath.ofproto

        actions = []


        try:
            nw_src = self.ipv4_text_to_int(ip_v4.src)
            nw_dst = self.ipv4_text_to_int(ip_v4.dst)
        except AssertionError, ex:
            self.logger.error("AssertionError: %s", str(ip_v4))

        match = datapath.ofproto_parser.OFPMatch(
                in_port=in_port,
                dl_type=eth.ethertype,
                dl_src=haddr_to_bin(eth.src),
                nw_proto=ip_v4.proto,
                nw_src=nw_src,
                nw_dst=nw_dst,
        )

        mod = datapath.ofproto_parser.OFPFlowMod(
            datapath=datapath, match=match, cookie=0,
            command=ofproto.OFPFC_ADD, idle_timeout=40, hard_timeout=40,
            priority=ofproto.OFP_DEFAULT_PRIORITY + 1,
            flags=ofproto.OFPFF_SEND_FLOW_REM, actions=actions)

        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        #switchIPAddress = ev.msg.datapath.socket.fd.getpeername()[0]
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto

        # Captura o pacote recebido pelo Controlador.
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        # Captura informacoes de IPv4 ou IPv6, TCP, UDP e ICMP, caso existam. Se o pacote
        # nao ter, a variavel recebera None
        ip_v4 = pkt.get_protocol(ipv4.ipv4)
        ip_v6 = pkt.get_protocol(ipv6.ipv6)
        tcp_port = pkt.get_protocol(tcp.tcp)
        udp_port = pkt.get_protocol(udp.udp)
        icmp_protocol = pkt.get_protocol(icmp.icmp)

        dst = eth.dst
        src = eth.src


        dpid = datapath.id

        self.mac_to_port.setdefault(dpid, {})

        # Log Packet-In
        #self.logger.info("Packet(%s) in %s %s %s %s", switchIPAddress, dpid, src, dst, msg.in_port)
        #self.logger.info(self.mac_to_port)
        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = msg.in_port


        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]

        if(ip_v4):
            # Verificando regras de controle parental no SGBD.
            lstDestIps = []
            lstOrigIps = []
            lstControls = self.session.query(Controls).filter(Controls.mac == src).first()

            if(lstControls):
                # Lista os enderecos de destino referentes ao perfil atribuido do MAC.
                lstBlacklists = self.session.query(ControlsBlacklists).filter(ControlsBlacklists.controls_id == lstControls.id).all()
                if(lstBlacklists):
                    for i in lstBlacklists:
                        lstIps = self.session.query(Ips).filter(Ips.blacklist_id == i.blacklist_id).all()
                        for j in lstIps:
                            lstDestIps.append(j.ip)

            
            if (ip_v4.dst in lstDestIps ) and (out_port != ofproto.OFPP_FLOOD):
                self.logger.info("# SOURCE # %s ===> # DESTINATION # %s  -  %s ###DROP###", src, dst, lstDestIps)
                self.add_flow_drop(datapath, msg.in_port, eth, ip_v4)
            else:
                lstControls = self.session.query(Controls).filter(Controls.mac == dst).first()

                if(lstControls):
                    # Lista os enderecos de destino referentes ao perfil atribuido do MAC.
                    lstBlacklists = self.session.query(ControlsBlacklists).filter(ControlsBlacklists.controls_id == lstControls.id).all()
                    if(lstBlacklists):
                        for i in lstBlacklists:
                            lstIps = self.session.query(Ips).filter(Ips.blacklist_id == i.blacklist_id).all()
                            for j in lstIps:
                                lstOrigIps.append(j.ip)
                if (ip_v4.src in lstOrigIps ) and (out_port != ofproto.OFPP_FLOOD):
                    self.logger.info("# SOURCE # %s ===> # DESTINATION # %s  -  %s ###DROP###", src, dst, lstDestIps)
                    self.add_flow_drop(datapath, msg.in_port, eth, ip_v4)
                else:
                    self.logger.info("# SOURCE # %s ===> # DESTINATION # %s  -  %s ###ACCEPT###", src, dst, lstDestIps)
                    self.add_flow(datapath, msg.in_port, eth, ip_v4, actions)
        else:
            # install a flow to avoid packet_in next time
            if out_port != ofproto.OFPP_FLOOD:
                self.logger.info("# SOURCE # %s ===> # DESTINATION # %s  ###ACCEPT###", eth.src, eth.dst)
                self.add_flow(datapath, msg.in_port, eth, ip_v4, actions)

        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath, buffer_id=msg.buffer_id,
            in_port=msg.in_port, actions=actions)

        datapath.send_msg(out)

    @set_ev_cls(ofp_event.EventOFPPortStatus, MAIN_DISPATCHER)
    def _port_status_handler(self, ev):
        msg = ev.msg
        reason = msg.reason
        port_no = msg.desc.port_no

        ofproto = msg.datapath.ofproto
        if reason == ofproto.OFPPR_ADD:
            self.logger.info("port added %s", port_no)
        elif reason == ofproto.OFPPR_DELETE:
            self.logger.info("port deleted %s", port_no)
        elif reason == ofproto.OFPPR_MODIFY:
            self.logger.info("port modified %s", port_no)
        else:
            self.logger.info("Illeagal port state %s %s", port_no, reason)
