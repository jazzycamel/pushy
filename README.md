# PushySDK

[![Build Status](https://travis-ci.org/jazzycamel/pushy.svg?branch=master)](https://travis-ci.org/jazzycamel/pushy)
[![Coverage Status](https://coveralls.io/repos/github/jazzycamel/pushy/badge.svg?branch=master)](https://coveralls.io/github/jazzycamel/pushy) 
[![PyPI version](https://badge.fury.io/py/PushySDK.svg)](https://badge.fury.io/py/PushySDK)

A very simple Python client for the Pushy notification service API.

## Installation

Simply install using pip:

```shell
$ pip install PushySDK
```

or clone this repository and run the following:

```shell
$ python setup.py install
```

You will need to install the following dependencies:

* requests
* six
* pypandoc

This can be done either manually or via pip with the included `requirements.txt` file as follows:

```shell
$ pip install -r requirements.txt
```

## Usage

You will first need to [signup](https://dashboard.pushy.me/) for a Pushy account and integrate the Pushy SDK into your Android and/or iOS mobile application (please refer to the comprehensive [Pushy Documentation](https://dashboard.pushy.me/)). Once you have successfully sent a test notification from the [Pushy Dashboard](https://dashboard.pushy.me/) you are ready to write some python!

First, get your application API key from the [Pushy Dashboard](https://dashboard.pushy.me/) (Applications > Your App > API Authentication). Once you have this you can then do the following:

```python
>>> from PushySDK import Pushy
>>> pushy=Pushy('<YOUR_API_KEY>')
```

You can now request information regarding a specific device (you can get device IDs from the [Pushy Dashboard](https://dashboard.pushy.me/)):

```python
>>> pushy.deviceInfo('<YOUR_DEVICE_ID>')
```

This will return a python dictionary object of information about the device as follows:

```python
{
    'device': {'date': 1445207358, 'platform': 'android'},
    'presence': {
         'online': True,
         'last_active': {'date': 1464006925, 'seconds_ago': 215}
    }, 
    pending_notifications': [
        {
            'date': 1464008196,
            'expiration': 1466600196,
            'payload': {'message': 'Hello World!'}, 'id': '5742fe0407c3674e226892f9'
        }
    ]
}
```

You can also return presence information for single or multiple devices as follows:

```python
>>> pushy.devicePresence(['<YOUR_DEVICE_ID>'])
{'presence': [
    {
        'online': False,
        'last_active': 1429406442,
        'id': 'a6f36efb913f1def30c6'
    },
    {
        'online': True,
        'last_active': 1468349965,
        'id': 'fe8f7b2c12e83e5b41d2'
    }
]}
```

To send a notification to a device or devices:

```python
>>> data={'message':'Hello from Python and Pushy!'}
>>> pushy.push('<YOUR_DEVICE_ID>', data)
>>> pushy.push(['<YOUR_DEVICE_ID_1>', '<YOUR_DEVICE_ID_2>'], data)
```

To add extra data for iOS [APNs](https://www.google.co.uk/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&cad=rja&uact=8&ved=0ahUKEwjUksWbhpLSAhXKWBoKHWJrDugQFgghMAE&url=https%3A%2F%2Fdeveloper.apple.com%2Fgo%2F%3Fid%3Dpush-notifications&usg=AFQjCNHPIGhIVb_jCDN7fWJYMdPeBKGIXw&sig2=8K65EutLZDTom2KcYjy0xQ) notifications, a utility function exists to form the request as follows:

```python
>>> title="Python/Pushy Notification"
>>> message='Hello from Python and Pushy!'
>>> badge=1
>>> sound="ping.aiff"
>>> apn=pushy.makeIOSNotification(message, badge, sound, title)
>>> pushy.push(['<YOUR_ANDROID_DEVICE_ID>', '<YOUR_IOS_DEVICE_ID>'], data, notification=apn)
```

The `push()` method will return a dictionary which reports the success or failure and a unique ID for the notification which can be used to track its status:

```python
{'success': True, 'id': '5742ea5dacf3a92e17ba7126'}
```

You can track a notifications status as follows:

```python
>>> pushy.notificationStatus('<YOUR_NOTIFICATION_ID>')
{
  "push": {
    "date": 1464003935,
    "payload": {
      "message": "Hello World!"
    },
    "expiration": 1466595935,
    "pending_devices": [
      "fe8f7b2c102e883e5b41d2"
    ]
  }
}
```
