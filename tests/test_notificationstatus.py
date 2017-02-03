from context import Pushy, getConfig, setupLogging

if __name__=="__main__":
    setupLogging()
    config=getConfig()
    p=Pushy.Pushy(config['api_key'])
    print("Notification Status: ", p.notificationStatus('5894717ddd41612e16bca9ac'))