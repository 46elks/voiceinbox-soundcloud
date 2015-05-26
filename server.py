#!/usr/bin/python
from gevent.pywsgi import WSGIServer
from gevent import monkey;
monkey.patch_all()
import urlparse
import soundcloud
import requests
import local


def application(env, start_response):
    data = urlparse.parse_qs(env["wsgi.input"].read());
    try:
        r = requests.get(data["wav"][0], auth=(local.user46elks, local.pass46elks))
        file = open(data["callid"][0]+'.wav', "w")
        file.write(r.content)
        file.close()
        
    except:
        start_response('500 Internal Server Error', [('Content-Type', 'application/json')])
        return 'Retrieving file from sender failed.'
    
    # Authenticate with Soundcloud
    try:
        client = soundcloud.Client(
            client_id=local.idsoundcloud,
            client_secret=local.secretsoundcloud,
            username=local.usersoundcloud,
            password=local.passsoundcloud
            )
            
    except:
        start_response('500 Internal Server Error', [('Content-Type', 'application/json')])
        return 'Unable to authenticate with soundcloud.'
    
    try:
        track = client.post(
            '/tracks', 
            track={
                'title': 'Voice recording from: '+data["from"][0],
                'asset_data': open(data["callid"][0]+'.wav', 'rb')
                }
            )
    except:
        start_response('500 Internal Server Error', [('Content-Type', 'application/json')])
        return 'Unable to upload to soundcloud.'
        
    start_response('200 OK', [('Content-Type', 'application/json')])
    return '{"result":"ok"}'
    
if __name__ == '__main__':
    print('Serving on 8989...')
    WSGIServer(('', 8989), application).serve_forever()


