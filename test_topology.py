"""Test Topology:

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.



        h1----s1----s2----s3
              |      |     |
        h3----s4----s5----s6
              |      |     |     
              s7----s8----s9---h2 

"""

from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        Host1 = self.addHost('h1')
        Host2 = self.addHost('h2')
        Host3 = self.addHost('h3')
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')
        s7 = self.addSwitch('s7')
        s8 = self.addSwitch('s8')
        s9 = self.addSwitch('s9')
        
        self.addLink( Host1, s1 )
        self.addLink( Host3, s4 )
        self.addLink( s1, s2 )
        self.addLink( s2, s3 )
        self.addLink( s1, s4 )
        self.addLink( s2, s5)
        self.addLink( s3, s6 )
        self.addLink( s4, s5 )
        self.addLink( s5, s6 )
        self.addLink( s4, s7 )
        self.addLink( s7, s8 )
        self.addLink( s5, s8 )
        self.addLink( s8, s9 )
        self.addLink( s6, s9 )
        self.addLink( s9, Host2 )
        
topos = { 'mytopo': ( lambda: MyTopo() ) }
