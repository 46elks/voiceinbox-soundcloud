#!/usr/bin/python
# -*- coding: utf-8 -*-

from gevent.pywsgi import WSGIServer
from gevent import monkey; monkey.patch_all()
import urlparse
import soundcloud
import requests
import local

# Handle incoming event:
def application(env, start_response):

    try:
        # read POST data:
        try:
            data = urlparse.parse_qs(env["wsgi.input"].read());
        except:
            raise Exception('POST request data error.')
   
        # GET sound File:
        try:
            r = requests.get(data["wav"][0], auth=(local.user46elks, local.pass46elks))
            file = open('soundfiles/'+data["callid"][0]+'.wav', "w")
            file.write(r.content)
            file.close()
        except:
            raise Exception('Retrieving file from sender failed.')
    
        # Authenticate with Soundcloud
        try:
            client = soundcloud.Client(
                client_id=local.idsoundcloud,
                client_secret=local.secretsoundcloud,
                username=local.usersoundcloud,
                password=local.passsoundcloud
                )
        except:
            raise Exception('Unable to authenticate with soundcloud.')
    
        # POST file to Soundcloud
        try:
            track = client.post(
                '/tracks', 
                track={
                    'title': 'Voice recording from: '+data["from"][0],
                    'asset_data': open('soundfiles/'+data["callid"][0]+'.wav', 'rb')
                    }
                )
        except:
            raise Exception('Unable to upload to soundcloud.')
    
    except Exception as e:
        start_response('500 Internal Server Error',[('content-type', 'text/html')])
        return e
    
    #success
    start_response('200 OK', [('Content-Type', 'application/json')])
    return '{"result":"ok"}'

# Run server    
if __name__ == '__main__':
    print('Serving on 8989...')
    WSGIServer(('', 8989), application).serve_forever()


