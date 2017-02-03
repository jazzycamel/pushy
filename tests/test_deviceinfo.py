from context import PushySDK, getConfig, setupLogging

if __name__=="__main__":
    setupLogging()
    config=getConfig()    
    p=PushySDK.Pushy(config['api_key'])
    print("Device Info: ", p.deviceInfo(config['device_token']))