from distutils.core import setup

setup(
    name='fse2017_robot',
    version='v0.1.0',
    packages=['fse_2017_robot',
              'fse_2017_robot.drivers',
              'fse_2017_robot.controllers'],
    url='https://fullstackembedded.com',
    license='GNU GPL',
    author='Daniel Lee',
    author_email='erget2005@gmail.com',
    description="Drivers and various driving aids for FSE 2017\'s Raspberry "
                "Pi-based robot."
)
