#sudo mn --custom ./custom_topo.py --topo mytopo --mac --switch ovsk --controller=remote,ip=192.168.0.102

from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        leftHost1 = self.addHost( 'h1' )
        leftHost2 = self.addHost( 'h2' )
        leftHost3 = self.addHost( 'h3' )
        rightHost1 = self.addHost( 'h4' )
        rightHost2 = self.addHost( 'h5' )
        leftSwitch = self.addSwitch( 's6' )
        rightSwitch = self.addSwitch( 's7' )

        # Add links
        self.addLink( leftHost1, leftSwitch )
        self.addLink( leftHost2, leftSwitch )
        self.addLink( leftHost3, leftSwitch )
        self.addLink( leftSwitch, rightSwitch )
        self.addLink( rightSwitch, rightHost1 )
        self.addLink( rightSwitch, rightHost2 )


topos = { 'mytopo': ( lambda: MyTopo() ) }
