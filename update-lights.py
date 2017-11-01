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
SENTINAL_BEGIN  = b'^'
SENTINAL_END    = b'$'
SERVER_ENDPOINT = 'http://space-bed-gcloud.appspot.com/current_color' 
SLEEP_TIME      = .5

# globals
current_color = 'OFF'

def main():
    
    global current_color
    ser = ''
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        ser.close()
        ser.open()
        time.sleep(2)
        print 'serial port is connected'
    except Exception as e:
        print 'Failed to connect to serial device'
    
    sys.stdout.flush()

    # main loop (escape on keyboard interrupt)
    try:
        while True:
            time.sleep(SLEEP_TIME)
            new_color = get_current_color()
            
            if new_color != current_color:
                print 'Setting color to:' + new_color +'!'
                sys.stdout.flush()
                msg   = SENTINAL_BEGIN + new_color + SENTINAL_END
                ser.write(msg.encode())
                time.sleep(SLEEP_TIME)
                current_color = new_color

    except KeyboardInterrupt:
        print 'Detected keyboard escape! Gracefully closing...'
        sys.exit(1)

def get_current_color():
    r = requests.get(SERVER_ENDPOINT)
    return r.text.upper().strip().encode()

if __name__ == "__main__":
    main()
