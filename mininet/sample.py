#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import OVSController
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def sampleNet():

    "Create an empty network and add nodes to it."

    net = Mininet( controller=OVSController )

    info( '*** Adding controller\n' )
    net.addController( 'c0' )

    info( '*** Adding hosts\n' )
    h1s1 = net.addHost( 'h1', ip='10.0.0.1' )
    h2s1 = net.addHost( 'h2', ip='10.0.0.3' )
    h1s2 = net.addHost( 'h1', ip='10.0.0.2' )
    h2s2 = net.addHost( 'h2', ip='10.0.0.4' )

    info( '*** Adding switches\n' )
    s1 = net.addSwitch( 's1' )
    s2 = net.addSwitch( 's2' )

    info( '*** Creating links\n' )
    pairs = [(h1s1, s1), (h2s1, s1), (h1s2, s2), (h2s2, s2)]
    [net.addLink( host, switch) for (host, switch) in pairs]

    info( '*** Starting network\n')
    net.start()

    info( '*** Starting HTTP server in h1s1')
    h1s1.cmd('python -m SimpleHTTPServer 8080')

    info( '*** Running CLI\n' )
    CLI( net )

    info( '*** Stopping network' )
    net.stop()

if __name__ == '__main__':
  setLogLevel( 'info' )
  sampleNet()
