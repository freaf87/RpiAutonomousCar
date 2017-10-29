# -*- coding: utf-8 -*-

"""TODO: Add headers to all files."""

from RpiAutonomousCar import Robot


class TestRobotMovement(object):
    """Interactive tests for robot motion."""

    def setup(self):
        self.r = Robot()

    def teardown(self):
        self.r.__exit__()

    def test_back_and_forth(self):
        """Test y-axis motion."""
        raw_input("DRIVE TEST: Clear path in front of and behind robot "
                  "for 5 cm and press Enter.")
        motions = [1, -2, 1]
        for motion in motions:
            self.r.drive(motion)
        report = raw_input("Did robot move as follows? {} \n"
                           "(Y/n): ".format(motions))
        assert(not report or report.lower() == 'y')

    def test_turning(self):
        """Test turning."""
        raw_input("TURN TEST: Press Enter when robot rotation is ready.")
        self.r.turn(45)
        self.r.turn(-450)
        self.r.turn(45)
        report = raw_input("Did robot turn 45° clockwise, then 450° "
                           "counterclockwise, then back to start? \n"
                           "(Y/n): ")
        assert(not report or report.lower() == 'y')


    def test_drive_arc(self):
        """Drive in arcs."""
        raw_input("ARC TEST: Clear ground 15cm to right and front and "
                  "press Enter.")
        self.r.drive_curve(2, 90)
        self.r.drive_curve(2, -90)
        self.r.turn(-135)
        self.r.drive(3.6)
        self.r.turn(135)
        report = raw_input("Did robot drive an arc to right, "
                           "then to left, then return to start? \n"
                           "(Y/n): ")
        assert(not report or report.lower() == 'y')

    def test_obstacle_detection(self):
        """Report obstacles correctly."""
        raw_input("ULTRASONIC TEST: Place obstacle within 20 cm of robot "
                  "and press Enter.")
        assert(self.r.obstacle < 20)
        raw_input("Clear ground before robot and press enter.")
        assert(self.r.obstacle > 20)


if __name__ == "__main__":
    suite = TestRobotMovement()
    try:
        suite.setup()
        tests = [fun for fun in dir(suite) if
                 callable(getattr(suite, fun)) and
                 fun.startswith("test")]
        for test in tests:
            try:
                getattr(suite, test)()
            except KeyboardInterrupt:
                print("\nSkipping test.")
    finally:
        suite.teardown()
