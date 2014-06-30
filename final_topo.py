#sudo mn --custom ./custom_topo.py --topo mytopo --mac --switch ovsk --controller=remote,ip=192.168.0.102

from mininet.topo import Topo

class MyTopo( Topo ):

    """

    # Data structure that must be inserted into the controller to represent this topology

    # Adjacency list of switches
    self.switches = {1: set([2,3,6,7,8]),
                     2: set([1,4,5,7]),
                     3: set([1,4,5,8]),
                     4: set([2,3,6,9]),
                     5: set([2,3,6,10]),
                     6: set([1,4,5,9,10]),
                     7: set([1,2]),
                     8: set([1,3]),
                     9: set([4,6]),
                     10: set([5,6])}

    # List of ports connecting other switches for each switch
    self.switches_ports = {9: {10: 4, 11: 5},
                           10: {9: 2, 13: 3},
                           11: {9: 2, 12: 3, 13: 4},
                           12: {11: 2},
                           13: {10: 3, 11: 4}}

    self.ip_to_switch_port = dict({'10.0.0.1': [9,1],
                                   '10.0.0.2': [9,2],
                                   '10.0.0.3': [9,3],
                                   '10.0.0.4': [10,1],
                                   '10.0.0.5': [11,1],
                                   '10.0.0.6': [12,1],
                                   '10.0.0.7': [13,1],
                                   '10.0.0.8': [13,2]})

    # Switch DPID [ip1..ipn]
    self.switch_ips = dict({9:['10.0.0.1','10.0.0.2', '10.0.0.3'],
                            10:['10.0.0.4'],
                            11:['10.0.0.5'],
                            12:['10.0.0.6'],
                            13:['10.0.0.7','10.0.0.8']})
    """

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        h1 = self.addHost( 'h1' )
        h2 = self.addHost( 'h2' )
        h3 = self.addHost( 'h3' )
        h4 = self.addHost( 'h4' )
        h5 = self.addHost( 'h5' )
        h6 = self.addHost( 'h6' )
        h7 = self.addHost( 'h7' )
        h8 = self.addHost( 'h8' )
        h9 = self.addHost( 'h9' )
        h10 = self.addHost( 'h10' )
        h11 = self.addHost( 'h11' )
        h12 = self.addHost( 'h12' )
        s9 = self.addSwitch( 's1' )
        s10 = self.addSwitch( 's2' )
        s11 = self.addSwitch( 's3' )
        s12 = self.addSwitch( 's4' )
        s13 = self.addSwitch( 's5' )
        s13 = self.addSwitch( 's6' )
        s13 = self.addSwitch( 's7' )
        s13 = self.addSwitch( 's8' )
        s13 = self.addSwitch( 's9' )
        s13 = self.addSwitch( 's10' )

        # Add links
        self.addLink( h1, s1 )
        self.addLink( h2, s2 )
        self.addLink( h3, s3 )
        self.addLink( h4, s4 )
        self.addLink( h5, s5 )
        self.addLink( h6, s6 )
        self.addLink( h7, s7 )
        self.addLink( h8, s8 )
        self.addLink( h9, s9 )
        self.addLink( h10, s10 )
        self.addLink( h11, s10 )
        self.addLink( h12, s10 )
        self.addLink( s1, s2 )
        self.addLink( s1, s3 )
        self.addLink( s1, s6 )
        self.addLink( s1, s7 )
        self.addLink( s1, s8 )
        self.addLink( s2, s4 )
        self.addLink( s2, s5 )
        self.addLink( s2, s7 )
        self.addLink( s3, s4 )
        self.addLink( s3, s5 )
        self.addLink( s3, s8 )
        self.addLink( s4, s6 )
        self.addLink( s4, s9 )
        self.addLink( s5, s6 )
        self.addLink( s5, s10 )
        self.addLink( s6, s9 )
        self.addLink( s6, s10 )
        


topos = { 'mytopo': ( lambda: MyTopo() ) }# 
