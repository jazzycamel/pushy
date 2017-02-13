# -*- coding: latin-1 -*-
import os, PushySDK

def getConfig():
    return dict(
        api_key=os.environ['PUSHY_API_KEY'],
        device_token_1=os.environ['PUSHY_DEV_TOK_1'],
        device_token_2=os.environ['PUSHY_DEV_TOK_2'],
    )

class TestClass:
    TEST_ID=None

    def test_one(self):
        config=getConfig()    
        p=PushySDK.Pushy(config['api_key'])
        r=p.deviceInfo(config['device_token_1'])
        assert 'device' in r

    def test_two(self):
        config=getConfig()
        p=PushySDK.Pushy(config['api_key'])
        r=p.devicePresence([config['device_token_1']])
        assert 'presence' in r

    def test_three(self):
        config=getConfig()
        p=PushySDK.Pushy(config['api_key'])

        title="Hello from Python Pushy"
        message="Hello from Python Pushy"
        badge=1
        sound="ping.aiff"
        notification=PushySDK.Pushy.makeIOSNotification(message, badge, sound, title)
        data=dict(message=message)

        r=p.push(config['device_token_1'], data, notification=notification, timeToLive=0)
        assert 'success' in r and r['success']==True
        TestClass.TEST_ID=r['id']

    def test_four(self):
        config=getConfig()
        p=PushySDK.Pushy(config['api_key'])

        title="Hello from Python Pushy"
        message="Hello from Python Pushy"
        badge=1
        sound="ping.aiff"
        notification=PushySDK.Pushy.makeIOSNotification(message, badge, sound, title)
        data=dict(message=message)
    
        r=p.push([config['device_token_1'], config['device_token_2']], data, notification=notification, timeToLive=0)
        assert 'success' in r and r['success']==True
        TestClass.TEST_ID=r['id']

    def test_five(self):
        config=getConfig()
        p=PushySDK.Pushy(config['api_key'])
        r=p.notificationStatus(TestClass.TEST_ID)
        assert 'push' in r