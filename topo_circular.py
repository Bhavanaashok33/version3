"""Test Topology:

   host1 --- leftSwitch --- centerSwitch --- rightSwitch --- host3
   host2 ------|
  
  
  
          --------s6------s7----------    
          |                          |   
   h1----s1----s2-----s3------s4----s5----h2
          |                          |
          -------------s8-------------       

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.

original,connected,weight
1,2,1
1,3,1
1,4,1
2,8,1
3,4,1
3,6,1
4,5,1
4,9,1
5,3,1
5,6,1
5,7,1
5,9,1
6,2,1
6,8,1
7,6,1
7,8,1
7,9,1
9,8,1

"""

from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )
###############################################3
        # Add hosts and switches
        Host1 = self.addHost( 'h1' )
        Host2 = self.addHost( 'h2' )
        s1 = self.addSwitch( 's1' )
        s2 = self.addSwitch( 's2' )
        s3 = self.addSwitch( 's3' )
        s4 = self.addSwitch( 's4' )
        s5 = self.addSwitch( 's5' )
        s7 = self.addSwitch('s7')
        s6 = self.addSwitch('s6')
        s8 = self.addSwitch('s8')
        s9 = self.addSwitch('s9')
        

       #  # Add links
       #
       
       
       

        self.addLink( Host1, s1 )
        self.addLink( s1, s2 )
        self.addLink( s1, s3 )
        self.addLink( s1, s4 )
        self.addLink( s2, s8)
        self.addLink( s3, s4 )
        self.addLink( s3, s6 )
        self.addLink( s4, s5 )
        self.addLink( s4, s9 )
       # 
        self.addLink( s5, s3 )
        self.addLink( s5, s6 )
        self.addLink( s5, s7 )
        self.addLink( s5, s9 )
        self.addLink( s6, s2 )
        self.addLink( s6, s8 )
        self.addLink( s7, s6 )
        self.addLink( s7, s8 )
        self.addLink( s7, s9 )
        self.addLink( s9, s8 )
        self.addLink( s9, Host2 )
######################################
        # Host1 = self.addHost( 'h1' )
        # Host2 = self.addHost( 'h2' )
        # s1 = self.addSwitch( 's1' )
        # s2 = self.addSwitch( 's2' )
        # s3 = self.addSwitch( 's3' )
        # s4 = self.addSwitch( 's4' )
        # s5 = self.addSwitch( 's5' )
        # s6 = self.addSwitch('s6')
        # s7 = self.addSwitch('s7')
        # s8 = self.addSwitch('s8')
        # s9 = self.addSwitch('s9')
        # 
        # # Add links
        # self.addLink( Host1, s1 )
        # self.addLink( s1, s2 )
        # self.addLink( s1, s4 )
        # self.addLink( s1, s3 )
        # 
        # self.addLink( s2, s8 )
        # self.addLink( s2, s6 )
        # 
        # self.addLink( s3, s6 )
        # self.addLink( s3, s4)
        # self.addLink( s3, s5 )
        # 
        # # self.addLink( s4, s9 )
        # self.addLink( s4, s5 )
        # 
        # 
        # self.addLink( s5, s9 )
        # self.addLink( s5, s6 )
        # self.addLink( s5, s7 )
        # 
        # self.addLink( s6, s7 )
        # self.addLink( s6, s8 )
        # 
        # 
        # self.addLink( s7, s8 )
        # self.addLink( s7, s9 )
        # 
        # 
        # self.addLink( s8, s9 )
        # 
        # self.addLink( s9, Host2 )
        # 


topos = { 'mytopo': ( lambda: MyTopo() ) }