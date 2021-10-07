from microbit import display,Image,sleep, button_a, button_b, running_time
from micropython import const
import radio 


import machine

DEVID = const("{:x}".format(int.from_bytes(machine.unique_id(), "big")))

radio.config(channel=12, group=12, length=64, queue=2, power=4)
radio.on()

_ELECTRON = (Image.ANGRY,[Image.ARROW_SE,"4",Image.DIAMOND_SMALL])
_PROTON = (Image.SILLY,[Image.ARROW_SW,"2",Image.DIAMOND])
_PHOTON = (Image.RABBIT,[Image.ARROW_S,"4", Image("0:0:00900:0:0")])
_NEUTRON = (Image.PACMAN,[Image.ARROW_S,"2", Image.DIAMOND])

_PARTICLES = [_ELECTRON,_PROTON,_PHOTON,_NEUTRON]


def _pop_or_none(arr):
    if arr and len(arr)>0:
      return arr.pop(0)
    else:
      return None

def ulp_parse(msg):
    meas = None
    tags = {}
    tmstp = None

    frags = msg.split(" ")
    frag = _pop_or_none(frags)
    if frag is not None:
        measFrags = frag.split(",")
        if len(measFrags) > 0:
            meas = measFrags[0]
        if  len(measFrags) > 1:
            for tagFrag in measFrags[1:]:
                tagKV = tagFrag.split("=")
                tags[tagKV[0]] = tagKV[1].strip('"\'')
    frag = _pop_or_none(frags)
    if frag is not None:
        tmstp = int(frag)
    return (meas, tags, tmstp)

def ulp_serialize(measurement, tags=None, timestamp=None): 
    result = measurement
    if tags is not None:
      for key, value in tags.items():
        result += ','+str(key)+"=\""+str(value)+"\""
    return result

def usquad_send(measurement, tags= {}, timestamp=None):
  tags["dev_id"] = DEVID
  msg = ulp_serialize(measurement, tags, timestamp)
  radio.send(msg)

def usquad_show(tags, timestamp=None):
  particle_idx = int(tags['p'])
  visual_idx = int(tags['v'])
  display.show(_PARTICLES[particle_idx][1][visual_idx], delay=1000, wait=True, clear=False)
  sleep(1000)

def usquad_vote(tags,timestamp=None):
  _vote(tags, [particle[0] for particle in _PARTICLES], timestamp)

def usquad_emote(tags,timestamp=None):
  _vote(tags, [Image.HEART,Image.SAD,Image.HAPPY,Image.SKULL], timestamp)

def usquad_heart(tags,timestamp=None):
  display.show(Image.HEART)

def _vote(tags,choices:list,timestamp=None):
  global incoming,METHOD_LIST
  _max_votes = int(tags.get('v',1))
  vote_cn = 0
  choices_max = len(choices)
  choice = 0
  button_a.get_presses()
  button_b.was_pressed()
  stopVote = False
  display.show(choices[choice], delay=50, clear=False,wait=True)
  while (not stopVote) and (vote_cn < _max_votes):
    a_presses = button_a.get_presses()
    if a_presses > 0:
      choice = (choice + a_presses) % choices_max
      display.show(choices[choice])
    if button_b.was_pressed():
      usquad_send("read_vote",{"value":choice, "index":vote_cn})
      display.show(Image.ARROW_N, wait=True, clear=False)
      sleep(300)
      vote_cn += 1
      votes_left = _max_votes - vote_cn
      if(votes_left > 0):
        display.show(str(votes_left), clear=False, wait=True)
        sleep(500)
        display.show(choices[choice], clear=False,wait=False)
    poll_messages()
    if incoming is not None and (not(incoming.startswith("read_") or incoming.startswith("bonjour"))) and (ulp_parse(incoming)[0] in METHOD_LIST):
      stopVote = True # keep incoming
  display.show(Image.YES)

def usquad_buttons(tags = None, timestamp=None):
  global incoming,METHOD_LIST
  button_a.was_pressed()
  button_b.was_pressed()
  display.show(Image.TRIANGLE)
  stopBtn = False
  while not stopBtn:
    if button_a.was_pressed():
      usquad_send("read_button",{"button":"a"})
      display.show("a")
    if button_b.was_pressed():
      usquad_send("read_button",{"button":"b"})
      display.show("b")
    poll_messages()
    if incoming is not None and (not(incoming.startswith("read_") or incoming == "bonjour")) and (ulp_parse(incoming)[0] in METHOD_LIST):
      stopBtn = True # keep incoming
    else:
      sleep(250)
      display.show(Image.SQUARE_SMALL)
      
  
METHOD_MAP = const({
  'show'           : usquad_show,
  'vote'           : usquad_vote,
  'buttons'        : usquad_buttons,
  'emote'          : usquad_emote,
  'heart'          : usquad_heart
})
METHOD_LIST = const(METHOD_MAP.keys())
incoming = None

def poll_messages():
  global incoming
  incoming = radio.receive()
  

# START AND MAIN LOOP
display.show(Image.HEART)
usquad_send("bonjour")

while True:
  meas = ""
  tags = ""
  stamp = 0
  
  poll_messages()

  while incoming is not None:
    if incoming.startswith("read_") or incoming.startswith("bonjour"):
      incoming = None # skip the message, it comes from another terminal
    else:
      meas,tags,stamp = ulp_parse(incoming)
      incoming = None
      execute = True
      if("dev_id" in tags.keys() and tags["dev_id"] != DEVID):
        execute = False
      method = METHOD_MAP.get(meas, None)
      if method is None:
        execute = False
      if execute:
        method(tags,stamp)
  sleep(100)