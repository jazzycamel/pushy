from context import PushySDK, getConfig, setupLogging

if __name__=="__main__":
    setupLogging()
    config=getConfig()
    p=PushySDK.Pushy(config['api_key'])
    print("Notification Status: ", p.notificationStatus('5894717ddd41612e16bca9ac'))