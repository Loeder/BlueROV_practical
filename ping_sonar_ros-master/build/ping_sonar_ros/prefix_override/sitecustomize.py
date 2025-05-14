import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/loeder/Documents/BlueRov/bluerov_ws/src/ping_sonar_ros-master/install/ping_sonar_ros'
