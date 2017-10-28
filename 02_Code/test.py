# -*- coding: utf-8 -*-

"""TODO: Add headers to all files."""

from RpiAutonomousCar import Robot


class TestRobotMovement(object):
    """Interactive tests for robot motion."""

    def setup(self):
        self.r = Robot()

    def teardown(self):
        self.r.destroy()

    def test_back_and_forth(self):
        """Test y-axis motion."""
        raw_input("Clear path in front of and behind robot for 5 cm "
                  "and press Enter.")
        motions = [1, -2, 1]
        for motion in motions:
            self.r.drive(motion)
        report = raw_input("Did robot move as follows? {} \n"
                           "(Y/n): ".format(motions))
        assert(not report or report.lower() == 'y')

    def test_turning(self):
        """Test turning."""
        raw_input("Press Enter when robot rotation is ready.")
        self.r.turn(45)
        self.r.turn(-450)
        self.r.turn(45)
        report = raw_input("Did robot turn 45° clockwise, then 450° "
                           "counterclockwise, then back to start? \n"
                           "(Y/n): ")
        assert(not report or report.lower() == 'y')

    def _test_drive_arc(self):
        """Drive in arcs."""
        print("Clear ground 15cm to right and front.")
        self.r.drive_curve(10, 90)
        self.r.drive_curve(10, -90)
        self.r.turn(-135)
        self.r.drive(18)
        self.r.turn(135)
        report = input("Did robot drive 10 cm arc to right, "
                       "then to left, then return to start? \n"
                       "(y/n): ")
        assert(report.lower() == 'y')

    def _test_obstacle_detection(self):
        """Report obstacles correctly."""
        raw_input("Place obstacle in front of robot and press enter.")
        assert(self.r.obstacle is not None)
        raw_input("Clear ground before robot and press enter.")
        assert(self.r.obstacle is None)


if __name__ == "__main__":
    suite = TestRobotMovement()
    try:
        suite.setup()
        tests = [fun for fun in dir(suite) if
                 callable(getattr(suite, fun)) and
                 fun.startswith("test")]
        for test in tests:
            getattr(suite, test)()
    finally:
        suite.teardown()
