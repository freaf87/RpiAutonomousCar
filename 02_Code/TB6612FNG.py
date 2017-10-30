#!/usr/bin/python
import time
import sys
import wiringpi as gpio

class TB6612FNG():
    """
    Class to represent TB6612FNG DC Motor driver
    """

    def __init__(self):
        # Initialise inputs & outputs pins
        self._M1Dir1Pin = 6
        self._M1Dir2Pin = 12
        self._M1PWMPin_annex  = 5  #solve error mapping (Vers.01)
        self._M1PWMPin  = 18
        self._M2Dir1Pin = 19
        self._M2Dir2Pin = 16
        self._M2PWMPin_annex  = 26 #solve error mapping (Vers.01)
        self._M2PWMPin = 13
        self._STBY =  20

        # Configure TB6612GNG Pins
        gpio.wiringPiSetupGpio ()
        gpio.pinMode(self._M1Dir1Pin,1)
        gpio.pinMode(self._M1Dir2Pin,1)
        gpio.pinMode(self._M1PWMPin,2)
        gpio.pinMode(self._M1PWMPin_annex, 0)
        gpio.pinMode(self._M2Dir1Pin,1)
        gpio.pinMode(self._M2Dir2Pin,1)
        gpio.pinMode(self._M2PWMPin,2)
        gpio.pinMode(self._M2PWMPin_annex, 0)
        gpio.pinMode(self._STBY, 1)

    def getDC(self, dc):
        return (1023*dc)/100

    def M1CounterClkwise(self):
        gpio.digitalWrite(self._M1Dir1Pin, 0)
        gpio.digitalWrite(self._M1Dir2Pin, 1)

    def M1Clkwise(self):
        gpio.digitalWrite(self._M1Dir1Pin, 1)
        gpio.digitalWrite(self._M1Dir2Pin, 0)

    def M2CounterClkwise(self):
        gpio.digitalWrite(self._M2Dir1Pin, 0)
        gpio.digitalWrite(self._M2Dir2Pin, 1)

    def M2Clkwise(self):
        gpio.digitalWrite(self._M2Dir1Pin, 1)
        gpio.digitalWrite(self._M2Dir2Pin, 0)

    def forward(self, dutyCycle = 20):
        self.M1CounterClkwise()
        self.M2Clkwise()
        gpio.pwmWrite(self._M1PWMPin, self.getDC(dutyCycle))
        gpio.pwmWrite(self._M2PWMPin, self.getDC(dutyCycle))
        gpio.digitalWrite(self._STBY, 1)

    def reverse(self, dutyCycle = 20):
        self.M1Clkwise()
        self.M2CounterClkwise()
        gpio.pwmWrite(self._M1PWMPin, self.getDC(dutyCycle))
        gpio.pwmWrite(self._M2PWMPin, self.getDC(dutyCycle))
        gpio.digitalWrite(self._STBY, 1)

    def right(self, dutyCycle = 20):
        self.M1CounterClkwise()
        self.M2CounterClkwise()
        gpio.pwmWrite(self._M1PWMPin, self.getDC(dutyCycle))
        gpio.pwmWrite(self._M2PWMPin, self.getDC(dutyCycle))
        gpio.digitalWrite(self._STBY, 1)

    def left(self, dutyCycle = 20):
        self.M1Clkwise()
        self.M2Clkwise()
        gpio.pwmWrite(self._M1PWMPin, self.getDC(dutyCycle))
        gpio.pwmWrite(self._M2PWMPin, self.getDC(dutyCycle))
        gpio.digitalWrite(self._STBY, 1)

    def stop(self):
        gpio.digitalWrite(self._M1Dir1Pin, 0)
        gpio.digitalWrite(self._M1Dir2Pin, 0)
        gpio.digitalWrite(self._M2Dir1Pin, 0)
        gpio.digitalWrite(self._M2Dir2Pin, 0)
        gpio.pwmWrite(self._M1PWMPin, 0)
        gpio.pwmWrite(self._M2PWMPin, 0)
        gpio.digitalWrite(self._STBY, 0)

    def destroy(self):
        gpio.pwmWrite(self._M1PWMPin , 0)
        gpio.pinMode (self._M1PWMPin , 0)
        gpio.pwmWrite(self._M2PWMPin , 0)
        gpio.pinMode (self._M2PWMPin , 0)
        gpio.pinMode (self._M1Dir1Pin, 0)
        gpio.pinMode (self._M1Dir2Pin, 0)
        gpio.pinMode (self._M2Dir1Pin, 0)
        gpio.pinMode (self._M2Dir2Pin, 0)


if __name__ == '__main__':
    tb6612fng = TB6612FNG()
    try:
        while True:

            print "forward"
            tb6612fng.forward()
            time.sleep(3)

            tb6612fng.stop()
            time.sleep(3)

            print "reverse"
            tb6612fng.reverse()
            time.sleep(3)

            tb6612fng.stop()
            time.sleep(3)

            print "left"
            tb6612fng.left()
            time.sleep(3)

            tb6612fng.stop()
            time.sleep(3)

            print "right"
            tb6612fng.right()
            time.sleep(3)

            tb6612fng.stop()
            time.sleep(3)
            print "Done!"

    except KeyboardInterrupt:
        tb6612fng.destroy()
        sys.exit(0)
