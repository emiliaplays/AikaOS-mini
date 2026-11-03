"""One-off live-CD video test using Firefox's local Marionette protocol."""
import json
from pathlib import Path
import socket
import subprocess
import sys
import time

class Marionette:
    def __init__(self):
        deadline=time.time()+150
        while True:
            try:
                self.socket=socket.create_connection(('127.0.0.1',2828),timeout=10)
                break
            except OSError:
                if time.time()>deadline: raise
                time.sleep(3)
        self.socket.settimeout(180)
        self.buffer=b''
        self.counter=0
        print('Greeting:',self.receive(),flush=True)

    def receive(self):
        while b':' not in self.buffer:
            chunk=self.socket.recv(65536)
            if not chunk: raise ConnectionError('Marionette connection closed')
            self.buffer+=chunk
        prefix,remaining=self.buffer.split(b':',1)
        length=int(prefix)
        while len(remaining)<length:
            chunk=self.socket.recv(65536)
            if not chunk: raise ConnectionError('Marionette connection closed')
            remaining+=chunk
        self.buffer=remaining[length:]
        return json.loads(remaining[:length])

    def command(self,name,parameters=None):
        self.counter+=1
        data=json.dumps([0,self.counter,name,parameters or {}],ensure_ascii=False).encode()
        self.socket.sendall(str(len(data)).encode()+b':'+data)
        while True:
            response=self.receive()
            if response[0]==1 and response[1]==self.counter:
                if response[2]: raise RuntimeError(json.dumps(response[2]))
                result=response[3]
                return result.get('value',result) if isinstance(result,dict) else result

    def js(self,script):
        return self.command('WebDriver:ExecuteScript',{'script':script,'args':[],'newSandbox':False,'sandbox':'default','line':1,'filename':'aika-live-video-test.py'})

browser=Marionette()
try: browser.command('WebDriver:DeleteSession')
except RuntimeError: pass
session=browser.command('WebDriver:NewSession',{'browserName':'firefox','pageLoadStrategy':'none','acceptInsecureCerts':False})
print('Session:',json.dumps(session),flush=True)
try: browser.command('WebDriver:MaximizeWindow')
except RuntimeError: pass
url=sys.argv[1] if len(sys.argv)>1 else 'https://www.youtube.com/watch?v=aqz-KE-bpKQ'
if url!='current': browser.command('WebDriver:Navigate',{'url':url})
result={'url':url,'pass':False,'samples':[]}
deadline=time.time()+300
clicked=False
while time.time()<deadline:
    try:
        state=browser.js(r'''
const buttons=Array.from(document.querySelectorAll('button'));
const reject=buttons.find(b=>/^(Reject all|Alle ablehnen|Tout refuser)$/i.test(b.innerText.trim().replace(/\s+/g,' ')));
if(reject) reject.click();
const skip=document.querySelector('.ytp-ad-skip-button,.ytp-ad-skip-button-modern');
if(skip) skip.click();
const v=document.querySelector('video');
const player=document.querySelector('#movie_player');
if(player && typeof player.setPlaybackQualityRange==='function') player.setPlaybackQualityRange('small','small');
if(v){v.muted=false;v.volume=0.25;if(v.paused)v.play().catch(e=>window.aikaPlayError=e.message);}
return {title:document.title,url:location.href,ready:document.readyState,
video:v?{time:v.currentTime,duration:v.duration,paused:v.paused,readyState:v.readyState,
width:v.videoWidth,height:v.videoHeight,decoded:v.mozDecodedFrames||(v.getVideoPlaybackQuality?v.getVideoPlaybackQuality().totalVideoFrames:0),presented:v.mozPresentedFrames,
hasAudio:v.mozHasAudio,muted:v.muted,volume:v.volume,
error:v.error?{code:v.error.code,message:v.error.message}:null,
ad:player?player.classList.contains('ad-showing'):false}:null,
playError:window.aikaPlayError||null,
formats:{vp9:document.createElement('video').canPlayType('video/webm; codecs="vp9, opus"'),h264:document.createElement('video').canPlayType('video/mp4; codecs="avc1.42E01E"')},
message:v?'':(document.body?document.body.innerText.slice(0,400):'')};
''')
        print('Video:',json.dumps(state,ensure_ascii=False),flush=True)
        result['samples'].append(state)
        video=state.get('video')
        sinks=json.loads(subprocess.check_output(['pactl','-f','json','list','sink-inputs'],text=True))
        result['audio_sink_inputs']=sinks
        firefox_audio=any('firefox' in json.dumps(sink).lower() for sink in sinks)
        if video and not clicked:
            browser.command('WebDriver:PerformActions',{'actions':[{'type':'pointer','id':'mouse','parameters':{'pointerType':'mouse'},'actions':[{'type':'pointerMove','duration':0,'origin':'viewport','x':400,'y':300},{'type':'pointerDown','button':0},{'type':'pointerUp','button':0}]}]})
            clicked=True
            time.sleep(3)
            continue
        if video and video['time']>8 and video['readyState']>=2 and video['width']>0 and video.get('decoded',0)>1 and (video.get('hasAudio') or firefox_audio) and not video.get('error') and not video.get('ad'):
            result['pass']=True
            result['successful_sample']=state
            break
    except (RuntimeError,TypeError) as error:
        print('Waiting:',error,flush=True)
    time.sleep(10)
try:
    result['audio_sink_inputs']=json.loads(subprocess.check_output(['pactl','-f','json','list','sink-inputs'],text=True))
except (subprocess.CalledProcessError,ValueError) as error:
    result['audio_check_error']=str(error)
Path('/tmp/aika-video-result.json').write_text(json.dumps(result,indent=2)+'\n')
print('AIKA_VIDEO_RESULT',json.dumps(result.get('successful_sample',{'pass':False})),flush=True)
raise SystemExit(0 if result['pass'] else 1)
