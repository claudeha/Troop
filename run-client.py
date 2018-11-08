#!/usr/bin/env python
"""
    Troop-Client
    ------------
    Real-time collaborative Live Coding.

    - Troop is a real-time collaborative tool that enables group live
      coding within the same document. To run the client application it
      must be able to connect to a running Troop Server instance on
      your network. Running `python run-client.py` will start the process
      of connecting to the server by asking for a host and port (defaults
      are localhost and port 57890). 

    - Using other Live Coding Languages:
    
        Troop is designed to be used with FoxDot (http://foxdot.org) but
        is also configured to work with Tidal Cycles (http://tidalcycles.org).
        You can run this file with the `--mode` flag followed by "tidalcycles"
        to use the Tidal Cycles language. You can also use any other application
        that can accept code commands as strings via the stdin by specifying
        the path of the interpreter application, such as ghci in the case of
        Tidal Cycles, in place of the "tidalcycles" string when using the
        `--mode` flag.
"""

import argparse

parser = argparse.ArgumentParser(
    prog="Troop Client", 
    description="Collaborative interface for Live Coding")

parser.add_argument('-i', '--cli', action='store_true', help="Use the command line to enter connection info")
parser.add_argument('-p', '--public', action='store_true', help="Connect to public Troop server")
parser.add_argument('-m', '--mode', action='store', default='foxdot',
                    help='Name of live coding language (TidalCycles, SonicPi, SuperCollider, FoxDot, or a valid path to an executable')
parser.add_argument('-c', '--config', action='store_true', help="Load connection info from 'client.cfg'")
parser.add_argument('-l', '--log', action='store_true')

# Add --host, --port?

args = parser.parse_args()

# Set up client

from src.client import Client
from src.config import readin
from getpass import getpass

# Client config options

options = { 'lang': args.mode, 'logging': args.log }

if args.public:

    from src.config import PUBLIC_SERVER_ADDRESS
    options['host'], options['port'] = PUBLIC_SERVER_ADDRESS  

elif args.cli:

    options['host']     = readin("Troop Server Address", default="localhost")
    options['port']     = readin("Port Number", default="57890")
    options['name']     = readin("Enter a name").replace(" ", "_")
    options['password'] = getpass()
    options['get_info'] = False

elif args.config:

    import os.path

    if os.path.isfile('client.cfg'):

        """
        You can set a configuration file if you are connecting to the same
        server on repeated occasions. A password should not be stored. The
        file (client.cfg) should look like:

        host=<host_ip>
        port=<port_no>

        """

        options['host'], options['port'] = Client.read_configuration_file('client.cfg')

    else:

        print("Unable to load configuration from 'client.cfg'")

myClient = Client(**options)