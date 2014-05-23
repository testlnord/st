__author__ = 'arkady'

import os
import sys

path_to_srv_config = "../src/"
path_to_srv_config = os.path.abspath(path_to_srv_config)

sys.path.append(path_to_srv_config)

#import config

port = '8080' #config.serverPort
host = '127.0.0.1'
