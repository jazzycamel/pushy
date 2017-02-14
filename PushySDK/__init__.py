import requests, logging, json, collections, six, logging
from functools import wraps

if six.PY3: basestring=str

logging.basicConfig()

def _processRequest(fn):
    @wraps(fn)
    def wrapper(self, tokens, *args, **kwargs):
        request=fn(self, tokens, *args, **kwargs)
        if request.status_code==requests.codes.ok:
            self._logger.info(
                "Successfully obtained {0} for device(s): {1}".format(fn.__name__, tokens))
            try: 
                response=request.json()
                if "error" in response:
                    self._logger.error("Failed to obtain {0} for device(s): {1} with error: {2}"
                        .format(fn.__name__, tokens, response['error']))
                    return None
                else: return response

            except ValueError as e:
                self._logger.error("Failed to parse JSON response: {0}".format(e))
                return None

        self._logger.error("Failed to get {0} for device(s): {1}, with HTTP Status Code: {2}"
            .format(fn.__name__, tokens, request.status_code))
        raise request.raise_for_status()
        return None 

    return wrapper

class Pushy(object):
    ONE_MONTH=2678400

    def __init__(self, key):
        self._key=key
        self._endpoint="https://api.pushy.me/"
        self._logger=logging.getLogger(__name__)

    @property
    def endpoint(self): return self._endpoint

    @endpoint.setter
    def endpoint(self, endpoint): self._endpoint=endpoint    

    @_processRequest
    def deviceInfo(self, token):
        params=dict(api_key=self._key)
        return requests.get(
            self._endpoint+'devices/{0}'.format(token),
            params=params
        )

    @_processRequest
    def devicePresence(self, tokens):
        params=dict(api_key=self._key)
        payload=dict(tokens=tokens)
        return requests.post(
            self._endpoint+"devices/presence",
            params=params,
            json=payload
        )

    @_processRequest
    def push(self, tokens, data, timeToLive=ONE_MONTH, notification=None, content_available=False):
        params=dict(api_key=self._key)
        payload=dict(data=data)

        if isinstance(tokens, basestring): payload['to']=tokens
        elif isinstance(tokens, collections.Sequence):
            if len(tokens)==1: payload['to']=tokens[0]
            elif len(tokens)>1: payload['tokens']=tokens

        if notification is not None:
            payload['notification']=notification
            payload['content_available']=content_available

        if timeToLive is not None:
            payload['time_to_live']=timeToLive

        return requests.post(
            self._endpoint+"push",
            params=params,
            json=payload
        )

    @staticmethod
    def makeIOSNotification(body, badge, sound, title):
        return dict(body=body, badge=badge, sound=sound, title=title)

    @_processRequest
    def notificationStatus(self, pushId):
        params=dict(api_key=self._key)
        return requests.get(
            self._endpoint+"pushes/{0}".format(pushId),
            params=params
        )