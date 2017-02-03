# -*- coding: latin-1 -*-
from context import Pushy, getConfig, setupLogging

if __name__=="__main__":
    setupLogging()
    config=getConfig()
    p=Pushy.Pushy(config['api_key'])

    title="Hello from Python Pushy 😜"
    message="Hello from Python Pushy"
    badge=1
    sound="ping.aiff"
    notification=Pushy.Pushy.makeIOSNotification(message, badge, sound, title)
    data=dict(message=message)

    print("Push: ", p.push(config['device_token'], data, notification=notification))
    print("Push: ", p.push([config['device_token']], data, notification=notification))