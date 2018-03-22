#! /usr/bin/env python

# Read the output of an Arduino which may be printing sensor output,
# and at the same time, monitor the user's input and send it to the Arduino.
# See also
# http://www.arcfn.com/2009/06/arduino-sheevaplug-cool-hardware.html

import sys, serial, select

class Arduino() :
    def run(self, port='/dev/tty.usbmodem1421', baud=115200):
        # Port may vary, so look for it:
        baseports = [port]
        self.ser = None
        for baseport in baseports:
            if self.ser : break
            for i in xrange(0, 8) :
                try :
                    port = baseport + str(i)
                    self.ser = serial.Serial(port, baud, timeout=1)
                    print "Opened", port
                    break
                except :
                    self.ser = None
                    pass

        if not self.ser :
            print "Couldn't open a serial port"
            sys.exit(1)

        self.ser.flushInput()
        while True :
            # Check whether the user has typed anything:
            inp, outp, err = select.select([sys.stdin, self.ser], [], [], .2)
            # Check for user input:
            if sys.stdin in inp :
                line = sys.stdin.readline()
                self.ser.write(line)
            # check for Arduino output:
            if self.ser in inp :
                line = self.ser.readline().strip()
                print "Arduino:", line

arduino = Arduino()
try :
    port = "/dev/tty.usbmodem142"
    baud = 115200
    if len(sys.argv) > 1: 
        print "Using port", sys.argv[1]
        port = sys.argv.pop()
    if len(sys.argv) > 1 :
        print "Using speed", sys.argv[1]
        baud = sys.argv.pop()
    arduino.run(baud=baud, port=port)
except serial.SerialException :
    print "Disconnected (Serial exception)"
except IOError :
    print "Disconnected (I/O Error)"
except KeyboardInterrupt :
    print "Interrupt"
