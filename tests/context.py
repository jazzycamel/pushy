import os, sys, json, logging
sys.path.insert(0, os.path.abspath('..'))

import PushySDK

def getConfig():
    with open("./test_config.json",'r') as f:
        return json.loads(f.read())

def setupLogging():
    FORMAT="%(name)s.%(module)s %(levelname)s: %(message)s"
    logging.basicConfig(format=FORMAT)