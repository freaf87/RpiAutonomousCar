import time
import RPi.GPIO as GPIO

class IRModule():
    def __init__(self):
        self._IRLeft   = 27
        self._IRMiddle = 18
        self._IRRight  = 17
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._IRLeft  ,GPIO.IN)
        GPIO.setup(self._IRMiddle,GPIO.IN)
        GPIO.setup(self._IRRight ,GPIO.IN)

    def getStatusLeft(self):
       return bool(GPIO.input(self._IRLeft))

    def getStatusMiddle(self):
        return bool(GPIO.input(self._IRMiddle))

    def getStatusRight(self):
        return bool(GPIO.input(self._IRRight))

    def destroy(self):
        GPIO.cleanup()

if __name__ == "__main__":

    IR = IRModule()
    try:
        while 1:
            statusLeft  = IR.getStatusLeft()
            statusMiddle  = IR.getStatusMiddle()
            statusRight = IR.getStatusRight()
            print "statusLeft   = "+ str(statusLeft)
            print "statusMiddle = "+ str(statusMiddle)
            print "statusRight  = "+ str(statusRight)
            time.sleep(1)

    except KeyboardInterrupt:
        IR.destroy()

