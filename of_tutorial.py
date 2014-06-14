# Copyright 2012 James McCauley
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This component is for use with the OpenFlow tutorial.

It acts as a simple hub, but can be modified to act like an L2
learning switch.

It's roughly similar to the one Brandon Heller did for NOX.
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt

log = core.getLogger()



class Tutorial (object):
  """
  A Tutorial object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

    # Use this table to keep track of which ethernet address is on
    # which switch port (keys are MACs, values are ports).
    self.mac_to_port = {}

    # Use this table to keep track of which IP address is on which
    # switch.
    # With option --mac on mininet, the switch number will be the
    # value of this mapping
    self.ip_to_switch = dict({'10.0.0.1': ['00:00:00:00:00:01', 'eth1'],
                            '10.0.0.2': ['00:00:00:00:00:01', 'eth2'],
                            '10.0.0.3': ['00:00:00:00:00:01', 'eth3']})

  def resend_packet (self, packet_in, out_port):
    """
    Instructs the switch to resend a packet that it had sent to us.
    "packet_in" is the ofp_packet_in object the switch had sent to the
    controller due to a table-miss.
    """
    msg = of.ofp_packet_out()
    msg.data = packet_in

    # Add an action to send to the specified port
    action = of.ofp_action_output(port = out_port)
    msg.actions.append(action)

    # Send message to switch
    self.connection.send(msg)


  def act_like_hub (self, packet, packet_in):
    """
    Implement hub-like behavior -- send all packets to all ports besides
    the input port.
    """

    # We want to output to all ports -- we do that using the special
    # OFPP_ALL port as the output port.  (We could have also used
    # OFPP_FLOOD.)
    self.resend_packet(packet_in, of.OFPP_ALL)

    # Note that if we didn't get a valid buffer_id, a slightly better
    # implementation would check that we got the full data before
    # sending it (len(packet_in.data) should be == packet_in.total_len)).


  def act_like_switch (self, packet, packet_in):
    """
    Implement switch-like behavior.
    """

    """ # DELETE THIS LINE TO START WORKING ON THIS (AND THE ONE BELOW!) #

    # Here's some psuedocode to start you off implementing a learning
    # switch.  You'll need to rewrite it as real Python code.

    # Learn the port for the source MAC
    self.mac_to_port ... <add or update entry>

    if the port associated with the destination MAC of the packet is known:
      # Send packet out the associated port
      self.resend_packet(packet_in, ...)

      # Once you have the above working, try pushing a flow entry
      # instead of resending the packet (comment out the above and
      # uncomment and complete the below.)

      log.debug("Installing flow...")
      # Maybe the log statement should have source/destination/port?

      #msg = of.ofp_flow_mod()
      #
      ## Set fields to match received packet
      #msg.match = of.ofp_match.from_packet(packet)
      #
      #< Set other fields of flow_mod (timeouts? buffer_id?) >
      #
      #< Add an output action, and send -- similar to resend_packet() >

    else:
      # Flood the packet out everything but the input port
      # This part looks familiar, right?
      self.resend_packet(packet_in, of.OFPP_ALL)

    """ # DELETE THIS LINE TO START WORKING ON THIS #

  def act_safely (self, packet, packet_in, event):
    """
    This is where the work resides! We need to make it distribute the package flow
    across different conections
    """
    ip = packet.find('ipv4')
    if ip is None:
      log.debug("Not IP package")
      # This packet isn't IP!

    src_ip = str(packet.payload.protosrc)
    dst_ip = str(packet.payload.protodst)
    log.debug("Src %s", src_ip)
    log.debug("Dst %s", dst_ip)

    log.debug("Switch src %s ", self.ip_to_switch[src_ip])    
    log.debug("Switch dst %s ", self.ip_to_switch[dst_ip])    

    log.debug("Here I am! %s" % packet.payload)
    log.debug("Wow! %s" % packet_in)
    log.debug("Ha! %s" % event)

  # This function will install a new OF rule in the given switch
  # also taking care of the destination of the package
  def install_rule(self, src_ip, dst_ip, switch):
    log.debug("Rule for %s -> %s at switch %s", src_ip, dst_ip, switch)

    # Handle cases where we don't have source IP or destination IP
    if src_ip == '0.0.0.0' or dst_ip == '0.0.0.0':
      log.warning("Src ou Dst IP not given!")
      return

    # Check if both hosts are connected in the same switch
    # In such case, we send the packages directly to the destination
    # The installed rule does not need to have expiration time
    if (self.ip_to_switch[src_ip][0] == self.ip_to_switch[dst_ip][0]):
      log.debug("SRC and DST are in the same switch")
      log.debug("SRC interface: %s", self.ip_to_switch[src_ip][1])
      log.debug("DST interface: %s", self.ip_to_switch[dst_ip][1])
      #self.connection.sendToDPID(switch, )
      

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.

    scr_ip = '0.0.0.0'
    dst_ip = '0.0.0.0'

    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    log.debug("Packet type %s", packet.type)

    # All possible package types are:
    # IP_TYPE, ARP_TYPE, RARP_TYPE, VLAN_TYPE, LLDP_TYPE, JUMBO_TYPE, QINQ_TYPE
    # Not sure if we need to handle all of these types.
    if packet.type == packet.ARP_TYPE:
      src_ip = str(packet.payload.protosrc)
      dst_ip = str(packet.payload.protodst)

    """
      if packet.payload.opcode == arp.REQUEST:

        arp_reply = arp()
        arp_reply.hwsrc = <requested mac address>
        arp_reply.hwdst = packet.src
        arp_reply.opcode = arp.REPLY
        arp_reply.protosrc = <IP of requested mac-associated machine>
        arp_reply.protodst = packet.payload.protosrc
        ether = ethernet()
        ether.type = ethernet.ARP_TYPE
        ether.dst = packet.src
        ether.src = <requested mac address>
        ether.payload = arp_reply
        #send this packet to the switch
        #see section below on this topic
      elif packet.payload.opcode == arp.REPLY:
        log.debug("It's a reply; do something cool")
      else:
        log.debug("Some other ARP opcode, probably do something smart here")
    """

    packet_in = event.ofp # The actual ofp_packet_in message.

    # self.connection.eth_addr # <- I dont know which of the methods to use!
    switch = str(self.connection.dpid)

    self.install_rule(src_ip, dst_ip, switch)
    # Comment out the following line and uncomment the one after
    # when starting the exercise.
    #self.act_like_hub(packet, packet_in)
    #self.act_like_switch(packet, packet_in)
    #self.act_safely(packet, packet_in, event)



def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Tutorial(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
