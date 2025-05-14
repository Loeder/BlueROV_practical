import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/loeder/Documents/BlueRov/bluerov_ws/src/install/autonomous_rov'
