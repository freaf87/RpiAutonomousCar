import time
import RPi.GPIO as GPIO


class SERVO():
    def __init__(self):
        self._ServoPin = 4
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._ServoPin, GPIO.OUT)
        self._ServoPWM = GPIO.PWM(self._ServoPin,50)
        self._ServoPWM.start(7.5)


    def loop(self):
        while True:
            self._ServoPWM.ChangeDutyCycle(7.5)
            time.sleep(1)
            self._ServoPWM.ChangeDutyCycle(12.5)
            time.sleep(1)
            self._ServoPWM.ChangeDutyCycle(2.5)
            time.sleep(1)

    def destroy(self):
        self._ServoPWM.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    servo = SERVO()
    try:
        servo.loop()
    except KeyboardInterrupt:
        servo.destroy()

