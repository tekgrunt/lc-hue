import limacharlie
import json
import gevent.signal
import signal
import sys
import getpass
import inspect
from phue import Bridge
from configparser import ConfigParser

config = ConfigParser()
config.read('./lc-hue.config')

oid = config.get('dev','oid')
secret_api_key = config.get('dev','secret_api_key')
bridge_ip = config.get('dev','bridge_ip')
user_token = config.get('dev','user_token')
bridge = Bridge( bridge_ip, user_token )

# This is an object we created to hold the lighting values associated with a given alert. There is also a time to live (TTL) 
# field that has not been implemented yet with the idea being after N seconds the lights go back to thier origianl state.
class AlertObject:
    def __init__( self, b, h, s, t ):
        self.brightness = b
        self.hue = h
        self.saturation = s
        self.ttl = t

# Here we are defining some tags and the associated colors
alert_level_dict = { 'macos': AlertObject( 254, 47084, 254, 10 ), 'windows': AlertObject( 254, 25600, 254, 10 ), 'linux': AlertObject( 254, 1625, 254, 10 )}

# brightness range: 0 - 254
# hue range: 0 - 65535
# saturation: 0 - 254
class SetLight:
    def __init__( self, light, alert_level ):
        light.brightness = alert_level.brightness
        light.saturation = alert_level.saturation
        light.hue = alert_level.hue

if __name__ == "__main__": 
    def signal_handler():
        global sp
        print( 'You pressed Ctrl+C!' )
        sp.shutdown()
        sys.exit( 0 )

    def debugPrint( msg ):
        print( msg )

    # If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
    bridge.connect()
    bridge.get_api()

    # Get the bridge state (This returns the full dictionary that you can explore)
    lights = bridge.lights

    # Save the initial state we find the lights in so we can revert after the TTL is implemented.
    initial_light_settings = []

    for l in lights: 
        initial_light_settings.append( AlertObject( l.brightness, l.saturation, l.hue, 0 )) 

    # Setting up the connection to LimaCharlie
    gevent.signal.signal( signal.SIGINT, signal_handler )
    man = limacharlie.Manager( oid, secret_api_key, print_debug_fn = debugPrint )
    sp = limacharlie.Spout( man, 'event' )

    # Monitor telemetry in real-time
    while True:
        data = sp.queue.get()
        routing = data['routing']
        tags = routing['tags']

        for tag in tags:
            if tag in alert_level_dict:                
                # Still need to implement the TTL for the light after it is set
                for l in lights:
                   SetLight(l, alert_level_dict[tag])

