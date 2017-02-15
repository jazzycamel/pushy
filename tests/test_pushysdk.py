# -*- coding: latin-1 -*-
import os, six, re, json, cgi, PushySDK

if six.PY3:
    from http.server import BaseHTTPRequestHandler, HTTPServer
    import urllib.parse as urlparse
elif six.PY2:
    from BaseHTTPServer import BaseHTTPRequestHandler
    from SocketServer import TCPServer as HTTPServer
    import urlparse

import socket
from threading import Thread
import requests

class MockServerRequestHandler(BaseHTTPRequestHandler):
    @staticmethod
    def getFreePort():
        s=socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
        s.bind(('localhost',0))
        a,p=s.getsockname()
        s.close()
        return p

    def do_GET(self):
        parsed=urlparse.urlparse(self.path)
        qs=urlparse.parse_qs(parsed.query)
        if parsed.path.startswith('/devices'):
            if 'api_key' in qs:
                if 'device_token_' not in parsed.path:
                    code=404
                    message=json.dumps({"error":"We could not find a device with that token linked to your account."})
                elif 'device_token_ok_fail' in parsed.path:
                    code=requests.codes.ok
                    message=json.dumps({"error":"We could not find a device with that token linked to your account."})
                elif 'device_token_bad_json' in parsed.path:
                    code=requests.codes.ok
                    message="{"
                else:
                    code=requests.codes.ok
                    message=json.dumps({
                        'presence': {
                            'online': True,
                            'last_active': {
                                'date': 1464006925,
                                'seconds_ago': 215
                            }
                        },
                        'device': {
                            'platform': 'android',
                            'date': 1445207358
                        },
                        'pending_notifications':[
                            {
                                'date': 1464008196,
                                'id': '5742fe0407c3674e226892f9',
                                'payload': {'message': 'Hello World!'},
                                'expiration': 1466600196
                            }
                        ]
                    })
        elif parsed.path.startswith('/pushes'):
            if 'api_key' in qs:
                code=requests.codes.ok
                message=json.dumps({
                    'push': {
                        'pending_devices': ['fe8f7b2c102e883e5b41d2'],
                        'date': 1464003935,
                        'expiration': 1466595935,
                        'payload': {'message': 'Hello World!'}
                    }
                })

        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        if six.PY3: message=bytes(message, 'utf-8')
        self.wfile.write(message)

    def do_POST(self):       
        ctype=self.headers['content-type']
        if ctype=='application/json':
            length=int(self.headers['content-length'])
            data=self.rfile.read(length)
            if six.PY3: data=data.decode('utf-8')
            data=json.loads(data)

            parsed=urlparse.urlparse(self.path)
            qs=urlparse.parse_qs(parsed.query)

            if parsed.path=='/devices/presence':
                if 'api_key' in qs:
                    code=requests.codes.ok
                    message=json.dumps({
                        'presence': [
                            {
                                'id': 'a6f36efb913f1def30c6',
                                'last_active': 1429406442,
                                'online': False
                            },
                            {
                                'id': 'fe8f7b2c12e83e5b41d2',
                                'last_active': 1468349965,
                                'online': True
                            }
                        ]
                    })

            if parsed.path=='/push':
                if 'api_key' in qs:
                    code=requests.codes.ok
                    message=json.dumps({"success":True, "id":"5742ea5dacf3a92e17ba7126"})

        self.send_response(code)
        self.end_headers()
        if six.PY3: message=bytes(message, 'utf-8')
        self.wfile.write(message)

class TestClass(object):
    TEST_ID=None

    @classmethod
    def setup_class(cls):
        cls._pushy=PushySDK.Pushy('api_key')

        cls._port=MockServerRequestHandler.getFreePort()
        cls._endpoint="http://localhost:{port}/".format(port=cls._port)

        cls._server=HTTPServer(('localhost', cls._port), MockServerRequestHandler)
        cls._thread=Thread(target=cls._server.serve_forever)
        cls._thread.setDaemon(True)
        cls._thread.start()

    def test_one(self):
        assert self._pushy.endpoint=='https://api.pushy.me/'

    def test_two(self):
        self._pushy.endpoint=self._endpoint
        assert self._pushy.endpoint==self._endpoint

    def test_three(self):
        r=self._pushy.deviceInfo('device_token_1')
        assert r is not None
        assert 'device' in r

    def test_four(self):
        r=self._pushy.devicePresence(['device_token_1','device_token_2'])
        assert r is not None

    def test_five(self):
        title="Hello from Python Pushy"
        message="Hello from Python Pushy"
        badge=1
        sound="ping.aiff"
        notification=PushySDK.Pushy.makeIOSNotification(message, badge, sound, title)
        data=dict(message=message)

        r=self._pushy.push('device_token_1', data, notification=notification, timeToLive=0)
        assert 'success' in r and r['success']==True
        TestClass.TEST_ID=r['id']

    def test_six(self):
        title="Hello from Python Pushy"
        message="Hello from Python Pushy"
        badge=1
        sound="ping.aiff"
        notification=PushySDK.Pushy.makeIOSNotification(message, badge, sound, title)
        data=dict(message=message)
    
        r=self._pushy.push(['device_token_1','device_token_2'], data, notification=notification, timeToLive=0)
        assert 'success' in r and r['success']==True
        TestClass.TEST_ID=r['id']

    def test_seven(self):
        r=self._pushy.notificationStatus(TestClass.TEST_ID)
        assert r is not None
        assert 'push' in r

    def test_eight(self):
        try: r=self._pushy.deviceInfo("bad_token")
        except requests.exceptions.HTTPError: assert True
        else: assert False

    def test_nine(self):
        assert self._pushy.deviceInfo('device_token_ok_fail')==None

    def test_ten(self):
        assert self._pushy.deviceInfo('device_token_bad_json')==None