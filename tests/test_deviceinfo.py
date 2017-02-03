from context import Pushy, getConfig, setupLogging

if __name__=="__main__":
    setupLogging()
    config=getConfig()    
    p=Pushy.Pushy(config['api_key'])
    print("Device Info: ", p.deviceInfo(config['device_token']))