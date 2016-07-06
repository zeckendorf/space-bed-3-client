################################################
###      Author: Sam Zeckendorf              ###
###        Date: 7/6/16                      ###
### Description: This is some really         ###
###              hacky code that pings       ###
###              a server to get the current ###
###              light state                 ###
################################################

# required libs
import requests
import serial
import time
import sys

# constants
SENTINAL_BEGIN  = '^'
SENTINAL_END    = '$'
SERVER_ENDPOINT = 'http://space-bed-gcloud.appspot.com/current_color' 
SLEEP_TIME      = .5

# globals
current_color = 'OFF'

def main():
    
    ser = ''
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        if not ser.isOpen():
            ser.open()
    except Exception as e:
        print 'Failed to connect to serial device'

    # main loop (escape on keyboard interrupt)
    try:
        while True:
            time.sleep(SLEEP_TIME)
            color = get_current_color()
            print 'Setting color to: ' + color
            msg   = SENTINAL_BEGIN + color + SENTINAL_END
            ser.write(msg.encode())
    except KeyboardInterrupt:
        print 'Detected keyboard escape! Gracefully closing...'
        sys.exit(1)

def get_current_color():
    r = requests.get(SERVER_ENDPOINT)
    return r.text

if __name__ == "__main__":
    main()
