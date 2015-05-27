# voiceinbox-soundcloud
Example of how to integrate recording of incoming calls to Soundcloud. 

## Usage

1 Rename local.py.template to local.py

2 Fill out data in local.py

3 Start server.py

4 Enter json for accoring to your needs on your 46elks number 'voice_start':

a. json code for recording a call after playing a sound: ````{
	"play":"http://url.path.to/sundfile.mp3",
	"next": 
	{
		"connect": "+46700000000",
		"recordcall": "http://your.server.com:8989"
	}
}````

b. json code for recording a call direclty, practical for outgoing calls: ````
	{
		"connect": "+46700000000",
		"recordcall": "http://your.server.com:8989"
	}````
  
c. json code for voicemail style recording: ````{
	"play": "http://myserver.se/entervoicemail.wav",
  	"next": {
    	"record": "http://your.server.com:8989"
  	}
}````
  
5 Call your number or make outgoing phonecall.
